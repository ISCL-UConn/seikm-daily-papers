#!/usr/bin/env python3
"""Build one issue of SEIKM Daily Papers.

    python3 scripts/run_daily.py                 # normal daily run
    python3 scripts/run_daily.py --dry-run       # harvest + classify, write nothing
    python3 scripts/run_daily.py --lookback 7    # widen the window (backfill)
    python3 scripts/run_daily.py --offline FILE  # classify a local JSON file
    python3 scripts/run_daily.py --date 2026-09-14

Exit codes: 0 success (including "quiet day, nothing new"), 1 failure.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from seikm import arxiv_source, render  # noqa: E402
from seikm.classify import assess_papers  # noqa: E402
from seikm.config import load_config  # noqa: E402
from seikm.enrich import enrich  # noqa: E402
from seikm.store import SeenStore  # noqa: E402


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Build one SEIKM Daily Papers issue")
    ap.add_argument("--dry-run", action="store_true",
                    help="harvest and classify but write no files")
    ap.add_argument("--lookback", type=int, default=None,
                    help="override harvest.lookback_days")
    ap.add_argument("--date", default=None, help="issue date (YYYY-MM-DD)")
    ap.add_argument("--offline", default=None,
                    help="classify papers from a local JSON file instead of arXiv")
    ap.add_argument("--no-llm", action="store_true", help="skip LLM enrichment")
    ap.add_argument("--allow-empty", action="store_true",
                    help="publish an issue even when nothing new cleared the bar")
    ap.add_argument("-v", "--verbose", action="store_true")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    log = logging.getLogger("seikm.run")

    config = load_config(ROOT / "config")
    issue_date = args.date or date.today().isoformat()

    # --- harvest ----------------------------------------------------------
    if args.offline:
        raw = json.loads(Path(args.offline).read_text(encoding="utf-8"))
        papers = raw["papers"] if isinstance(raw, dict) else raw
        log.info("offline mode: %d papers from %s", len(papers), args.offline)
    else:
        hcfg = dict(config.harvest)
        if args.lookback:
            hcfg["lookback_days"] = args.lookback
        papers = arxiv_source.harvest(hcfg)
    scanned = len(papers)
    log.info("harvested %d unique papers", scanned)

    # --- dedupe against past issues --------------------------------------
    store = SeenStore(ROOT / "data" / "seen.json")
    fresh = store.filter_new(papers)
    log.info("%d are new (%d already published)", len(fresh), scanned - len(fresh))

    # --- classify ---------------------------------------------------------
    kept = assess_papers(config, fresh)
    log.info("%d cleared the relevance gate and topic threshold", len(kept))

    selected = render.select_for_issue(config, kept)
    log.info("%d selected for this issue (caps applied)", len(selected))

    if not args.no_llm:
        selected = enrich(config, selected)
    selected.sort(key=lambda p: p.get("rank_score", p.get("score", 0)), reverse=True)

    by_topic: dict[str, int] = {}
    for p in selected:
        by_topic[p["topic"]] = by_topic.get(p["topic"], 0) + 1
    for code, n in sorted(by_topic.items()):
        log.info("  %-11s %d", code, n)

    if args.dry_run:
        log.info("dry run: no files written")
        for p in selected[:15]:
            log.info("  %-11s %5.1f  %s", p["topic"], p.get("rank_score", 0),
                     p["title"][:78])
        return 0

    # --- quiet day --------------------------------------------------------
    # Publishing a zero-paper issue would clutter the archive and overwrite the
    # homepage with an empty page. Nothing is written, nothing is marked seen,
    # and tomorrow's wider lookback window picks up anything that appears late.
    if not selected and not args.allow_empty:
        log.info("nothing new cleared the bar today; leaving the last issue in "
                 "place (use --allow-empty to publish anyway)")
        return 0

    # --- write ------------------------------------------------------------
    issue = {
        "date": issue_date,
        "number": store.issue_number(issue_date),
        "count": len(selected),
        "scanned": scanned,
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }

    (ROOT / "digests").mkdir(exist_ok=True)
    md = render.render_markdown(config, issue, selected)
    (ROOT / "digests" / f"{issue_date}.md").write_text(md, encoding="utf-8")

    store.record_issue({"date": issue["date"], "number": issue["number"],
                        "count": issue["count"], "scanned": scanned})
    issues = store.issues

    docs = ROOT / "docs"
    (docs / "archive").mkdir(parents=True, exist_ok=True)
    (docs / ".nojekyll").touch()

    recent = issues[: int(config.output["recent_issues_on_home"])]
    (docs / "index.html").write_text(
        render.render_issue_html(config, issue, selected, rel="", recent=recent[1:],
                                 is_home=True),
        encoding="utf-8")
    (docs / "archive" / f"{issue_date}.html").write_text(
        render.render_issue_html(config, issue, selected, rel="../"),
        encoding="utf-8")
    (docs / "archive" / "index.html").write_text(
        render.render_archive_html(config, issues), encoding="utf-8")
    (docs / "feed.xml").write_text(
        render.render_feed(config, issues, selected), encoding="utf-8")
    (docs / "latest.json").write_text(
        json.dumps({"issue": issue, "papers": [
            {k: p.get(k) for k in ("id", "title", "authors", "abs_url", "pdf_url",
                                   "topic", "secondary_topics", "score", "rank_score",
                                   "primary_category", "why")}
            for p in selected]}, indent=1),
        encoding="utf-8")

    readme_path = ROOT / "README.md"
    if readme_path.exists():
        block = render.render_readme_block(config, issue, selected)
        readme_path.write_text(
            render.splice_readme(readme_path.read_text(encoding="utf-8"), block),
            encoding="utf-8")

    store.mark(fresh, date.fromisoformat(issue_date))
    pruned = store.prune(date.fromisoformat(issue_date))
    if pruned:
        log.info("pruned %d aged entries from the seen database", pruned)
    store.save()

    log.info("issue #%d written: %d papers", issue["number"], len(selected))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
