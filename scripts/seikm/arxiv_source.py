"""arXiv harvesting.

Uses only the standard library so the workflow has one dependency (PyYAML).

Two kinds of query:

  sweep    cat:cs.CE          -- categories where most papers are plausibly
                                 in scope, pulled wholesale.
  phrase   (cat:A OR cat:B) AND all:"digital twin"
                              -- high-signal hooks into the broad ML/CS
                                 categories, which are far too noisy to sweep.

arXiv asks for a descriptive User-Agent and roughly one request every three
seconds; both are honoured here.
"""
from __future__ import annotations

import logging
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from typing import Any, Iterable

from .textclean import clean_authors, detex

log = logging.getLogger("seikm.arxiv")

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
USER_AGENT = (
    "SEIKM-Daily-Papers/1.0 (ASME IDETC-CIE SEIKM technical committee digest; "
    "+https://github.com/ISCL-UConn/seikm-daily-papers)"
)


def _text(node: ET.Element | None) -> str:
    if node is None or node.text is None:
        return ""
    return " ".join(node.text.split())


def _parse_entry(entry: ET.Element) -> dict[str, Any] | None:
    raw_id = _text(entry.find("a:id", NS))
    if not raw_id:
        return None
    # http://arxiv.org/abs/2509.12345v2  ->  ("2509.12345", 2)
    tail = raw_id.rsplit("/abs/", 1)[-1]
    version = 1
    arxiv_id = tail
    if "v" in tail:
        base, _, v = tail.rpartition("v")
        if v.isdigit():
            arxiv_id, version = base, int(v)

    published = _text(entry.find("a:published", NS))
    updated = _text(entry.find("a:updated", NS))
    authors = clean_authors(
        [_text(a.find("a:name", NS)) for a in entry.findall("a:author", NS)])
    cats = [c.get("term", "") for c in entry.findall("a:category", NS)]
    prim = entry.find("arxiv:primary_category", NS)
    primary = prim.get("term", "") if prim is not None else (cats[0] if cats else "")

    pdf = ""
    for link in entry.findall("a:link", NS):
        if link.get("title") == "pdf":
            pdf = link.get("href", "")

    return {
        "id": arxiv_id,
        "version": version,
        "title": detex(_text(entry.find("a:title", NS))),
        "abstract": detex(_text(entry.find("a:summary", NS))),
        "authors": authors,
        "published": published,
        "updated": updated,
        "primary_category": primary,
        "categories": cats,
        "abs_url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": pdf or f"https://arxiv.org/pdf/{arxiv_id}",
        "doi": _text(entry.find("arxiv:doi", NS)),
        "comment": _text(entry.find("arxiv:comment", NS)),
        "journal_ref": _text(entry.find("arxiv:journal_ref", NS)),
    }


def _fetch(query: str, max_results: int, timeout: int, retries: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    url = f"{API}?{params}"
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = resp.read()
            root = ET.fromstring(payload)
            entries = [_parse_entry(e) for e in root.findall("a:entry", NS)]
            return [e for e in entries if e]
        except (urllib.error.URLError, ET.ParseError, OSError) as exc:
            last_err = exc
            wait = min(60, 5 * attempt * attempt)
            log.warning("query failed (attempt %d/%d): %s; retrying in %ds",
                        attempt, retries, exc, wait)
            time.sleep(wait)
    log.error("giving up on query %r: %s", query[:90], last_err)
    return []


def build_queries(harvest: dict[str, Any]) -> list[tuple[str, str]]:
    """Return (label, arxiv_query) pairs."""
    queries: list[tuple[str, str]] = []
    for cat in harvest.get("sweep_categories", []):
        queries.append((f"sweep:{cat}", f"cat:{cat}"))

    filtered = harvest.get("filtered_categories", [])
    if filtered:
        cat_clause = "(" + " OR ".join(f"cat:{c}" for c in filtered) + ")"
        for phrase in harvest.get("phrase_queries", []):
            queries.append((f"phrase:{phrase}", f'{cat_clause} AND all:"{phrase}"'))
    return queries


def _recent(paper: dict[str, Any], cutoff: datetime) -> bool:
    stamp = paper.get("published") or paper.get("updated")
    if not stamp:
        return False
    try:
        dt = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return False
    return dt >= cutoff


def harvest(harvest_cfg: dict[str, Any], *, now: datetime | None = None) -> list[dict[str, Any]]:
    """Run every query, keep recent papers, dedupe by arXiv id."""
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=int(harvest_cfg.get("lookback_days", 3)))
    delay = float(harvest_cfg.get("request_delay_seconds", 3.5))
    timeout = int(harvest_cfg.get("timeout_seconds", 60))
    retries = int(harvest_cfg.get("retries", 4))
    per_query = int(harvest_cfg.get("per_query_max", 120))

    queries = build_queries(harvest_cfg)
    log.info("running %d arXiv queries (lookback %s)", len(queries), cutoff.date())

    give_up_after = int(harvest_cfg.get("abandon_after_failures", 3))
    consecutive_failures = 0

    by_id: dict[str, dict[str, Any]] = {}
    for i, (label, query) in enumerate(queries, 1):
        rows = _fetch(query, per_query, timeout, retries)
        if not rows:
            consecutive_failures += 1
            if consecutive_failures >= give_up_after:
                log.error(
                    "%d consecutive queries returned nothing; abandoning the API "
                    "source. arXiv rate-limits shared cloud IPs, so this is "
                    "expected on CI runners -- RSS is the supported path.",
                    consecutive_failures)
                break
        else:
            consecutive_failures = 0
        fresh = [r for r in rows if _recent(r, cutoff)]
        for row in fresh:
            existing = by_id.get(row["id"])
            if existing is None:
                row["found_via"] = [label]
                by_id[row["id"]] = row
            elif label not in existing["found_via"]:
                existing["found_via"].append(label)
        log.info("[%2d/%d] %-46s %3d returned, %3d recent, %4d unique so far",
                 i, len(queries), label[:46], len(rows), len(fresh), len(by_id))
        if i < len(queries):
            time.sleep(delay)

    papers = list(by_id.values())
    papers.sort(key=lambda p: p.get("published", ""), reverse=True)
    return papers
