"""The seen-papers database.

A flat id -> first-seen-date map. Two jobs:
  * never show the same paper twice, even though lookback_days > 1 means a
    paper is harvested on several consecutive runs;
  * let a failed or skipped run self-heal the next day without duplicating.

Entries older than `retention_days` are pruned so the file stays small enough
to live in git comfortably.
"""
from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable


class SeenStore:
    def __init__(self, path: Path, retention_days: int = 180) -> None:
        self.path = path
        self.retention_days = retention_days
        self.ids: dict[str, str] = {}
        self.issues: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        self.ids = dict(data.get("ids", {}))
        self.issues = list(data.get("issues", []))

    def is_new(self, arxiv_id: str) -> bool:
        return arxiv_id not in self.ids

    def filter_new(self, papers: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
        return [p for p in papers if self.is_new(p["id"])]

    def mark(self, papers: Iterable[dict[str, Any]], on: date) -> None:
        stamp = on.isoformat()
        for p in papers:
            self.ids.setdefault(p["id"], stamp)

    def record_issue(self, issue: dict[str, Any]) -> None:
        self.issues = [i for i in self.issues if i.get("date") != issue["date"]]
        self.issues.append(issue)
        self.issues.sort(key=lambda i: i["date"], reverse=True)

    def issue_number(self, for_date: str) -> int:
        dates = sorted({i["date"] for i in self.issues} | {for_date})
        return dates.index(for_date) + 1

    def prune(self, today: date) -> int:
        cutoff = (today - timedelta(days=self.retention_days)).isoformat()
        before = len(self.ids)
        self.ids = {k: v for k, v in self.ids.items() if v >= cutoff}
        return before - len(self.ids)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "count": len(self.ids),
            "issues": self.issues,
            "ids": dict(sorted(self.ids.items())),
        }
        self.path.write_text(json.dumps(payload, indent=1, sort_keys=False) + "\n",
                             encoding="utf-8")
