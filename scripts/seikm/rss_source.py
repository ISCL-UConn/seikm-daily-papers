"""arXiv RSS harvesting — the primary source.

Why RSS and not the search API
------------------------------
arXiv's export API (export.arxiv.org) rate-limits shared cloud IP ranges hard,
and GitHub Actions runners sit squarely in one. In practice the very first
query comes back HTTP 429 regardless of pacing, because the runner's address is
already hot from other users.

rss.arxiv.org is a different, CDN-backed host built to be polled, and it serves
the full daily "new submissions" listing for any combination of categories in a
single request. That is strictly better for this job: two requests instead of
thirty-four, complete coverage of every category we care about, and the
filtering happens locally in the classifier we already have.

The trade-off is that RSS carries only the most recent announcement, with no
lookback. `arxiv_source.py` remains available as a backfill path for the rare
case where that matters.

arXiv announces Sunday through Thursday at 20:00 US Eastern. Outside that
window the feeds are legitimately empty, which is a quiet day and not an error.
"""
from __future__ import annotations

import logging
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any

from .textclean import clean_authors, detex

log = logging.getLogger("seikm.rss")

BASE = "https://rss.arxiv.org/atom/"
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
    "dc": "http://purl.org/dc/elements/1.1/",
}
USER_AGENT = (
    "SEIKM-Daily-Papers/1.0 (ASME IDETC-CIE SEIKM technical committee digest; "
    "+https://github.com/ISCL-UConn/seikm-daily-papers)"
)

# "arXiv:2509.12345v1 Announce Type: new \nAbstract: ..." -> the abstract.
# Every part is optional: arXiv has shipped entries without the announce-type
# line, and stripping only some of the preamble is worse than stripping none.
_PREAMBLE = re.compile(
    r"^\s*(?:arxiv:\s*\S+\s*)?(?:announce\s+type:\s*[\w-]+\s*)?(?:abstract:\s*)?",
    re.IGNORECASE,
)
_ID_IN_TEXT = re.compile(r"(\d{4}\.\d{4,5})(?:v(\d+))?")


def _text(node: ET.Element | None) -> str:
    if node is None or node.text is None:
        return ""
    return " ".join(node.text.split())


def _raw(node: ET.Element | None) -> str:
    if node is None or node.text is None:
        return ""
    return node.text


def _parse_authors(entry: ET.Element) -> list[str]:
    """arXiv packs the whole author list into one <name>, comma separated."""
    names: list[str] = []
    for author in entry.findall("a:author", NS):
        raw = _text(author.find("a:name", NS))
        if raw:
            names.extend(p.strip() for p in raw.split(",") if p.strip())
    if not names:
        for creator in entry.findall("dc:creator", NS):
            raw = _text(creator)
            names.extend(p.strip() for p in raw.split(",") if p.strip())
    return clean_authors(names)


def _parse_entry(entry: ET.Element) -> dict[str, Any] | None:
    # The id looks like "oai:arXiv.org:2509.12345v1"; fall back to the link.
    ident = _text(entry.find("a:id", NS))
    link_el = entry.find("a:link", NS)
    href = link_el.get("href", "") if link_el is not None else ""
    summary_raw = _raw(entry.find("a:summary", NS))

    match = _ID_IN_TEXT.search(ident) or _ID_IN_TEXT.search(href) \
        or _ID_IN_TEXT.search(summary_raw[:120])
    if not match:
        return None
    arxiv_id = match.group(1)
    version = int(match.group(2)) if match.group(2) else 1

    title = detex(_text(entry.find("a:title", NS)))
    abstract = detex(" ".join(_PREAMBLE.sub("", summary_raw).split()))
    if not title or not abstract:
        return None

    announce = _text(entry.find("arxiv:announce_type", NS)).lower() or "new"
    cats = [c.get("term", "") for c in entry.findall("a:category", NS) if c.get("term")]
    published = _text(entry.find("a:published", NS)) or _text(entry.find("a:updated", NS))

    return {
        "id": arxiv_id,
        "version": version,
        "title": title,
        "abstract": abstract,
        "authors": _parse_authors(entry),
        "published": published,
        "updated": _text(entry.find("a:updated", NS)) or published,
        "primary_category": cats[0] if cats else "",
        "categories": cats,
        "abs_url": href or f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
        "doi": "",
        "comment": "",
        "journal_ref": "",
        "announce_type": announce,
    }


def _fetch(url: str, timeout: int, retries: int) -> bytes | None:
    last: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except (urllib.error.URLError, OSError) as exc:
            last = exc
            wait = min(45, 5 * attempt)
            log.warning("feed fetch failed (attempt %d/%d): %s; retrying in %ds",
                        attempt, retries, exc, wait)
            time.sleep(wait)
    log.error("giving up on %s: %s", url, last)
    return None


def harvest(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Fetch the current announcement across every configured category."""
    categories: list[str] = list(cfg.get("rss_categories") or [])
    if not categories:
        log.warning("no rss_categories configured")
        return []

    batch = max(1, int(cfg.get("rss_batch_size", 8)))
    timeout = int(cfg.get("timeout_seconds", 60))
    retries = int(cfg.get("retries", 4))
    delay = float(cfg.get("rss_delay_seconds", 2.0))
    keep = {t.lower() for t in (cfg.get("announce_types") or ["new", "cross"])}

    groups = [categories[i : i + batch] for i in range(0, len(categories), batch)]
    by_id: dict[str, dict[str, Any]] = {}
    skipped_type = 0
    unparsed = 0

    for i, group in enumerate(groups, 1):
        url = BASE + "+".join(group)
        payload = _fetch(url, timeout, retries)
        if payload is None:
            continue
        try:
            root = ET.fromstring(payload)
        except ET.ParseError as exc:
            log.error("feed %d did not parse: %s", i, exc)
            continue

        entries = root.findall("a:entry", NS)
        kept = 0
        for entry in entries:
            row = _parse_entry(entry)
            if row is None:
                unparsed += 1
                continue
            if row["announce_type"] not in keep:
                skipped_type += 1
                continue
            existing = by_id.get(row["id"])
            if existing is None:
                row["found_via"] = [f"rss:{'+'.join(group)}"]
                by_id[row["id"]] = row
                kept += 1
            else:
                tag = f"rss:{'+'.join(group)}"
                if tag not in existing["found_via"]:
                    existing["found_via"].append(tag)

        log.info("[%d/%d] %-44s %3d entries, %3d kept, %4d unique so far",
                 i, len(groups), "+".join(group)[:44], len(entries), kept, len(by_id))
        if i < len(groups):
            time.sleep(delay)

    if skipped_type:
        log.info("skipped %d entries by announce type (kept: %s)",
                 skipped_type, ", ".join(sorted(keep)))
    if unparsed:
        log.warning("%d entries could not be parsed and were skipped", unparsed)
    if not by_id:
        log.info("feeds are empty — arXiv announces Sun-Thu at 20:00 US Eastern, "
                 "so this is expected outside that window")

    papers = list(by_id.values())
    papers.sort(key=lambda p: p.get("published", ""), reverse=True)
    return papers
