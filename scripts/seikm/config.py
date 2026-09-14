"""Config loading with light validation."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = REPO_ROOT / "config"


def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not parse to a mapping")
    return data


@dataclass
class Topic:
    code: str
    slug: str
    title: str
    short: str
    scope: str
    strong: list[str] = field(default_factory=list)
    medium: list[str] = field(default_factory=list)
    weak: list[str] = field(default_factory=list)

    def tiered_terms(self) -> list[tuple[str, str]]:
        out: list[tuple[str, str]] = []
        for tier in ("strong", "medium", "weak"):
            for term in getattr(self, tier):
                out.append((term, tier))
        return out


@dataclass
class Config:
    settings: dict[str, Any]
    topics: list[Topic]
    general: Topic

    @property
    def site(self) -> dict[str, Any]:
        return self.settings["site"]

    @property
    def harvest(self) -> dict[str, Any]:
        return self.settings["harvest"]

    @property
    def scoring(self) -> dict[str, Any]:
        return self.settings["scoring"]

    @property
    def gate(self) -> dict[str, Any]:
        return self.settings["gate"]

    @property
    def veto(self) -> dict[str, Any]:
        return self.settings["veto"]

    @property
    def output(self) -> dict[str, Any]:
        return self.settings["output"]

    @property
    def llm(self) -> dict[str, Any]:
        return self.settings.get("llm", {"enabled": False})

    @property
    def committee_topic_count(self) -> int:
        return len(self.topics)

    def topic_by_code(self, code: str) -> Topic:
        for topic in self.topics:
            if topic.code == code:
                return topic
        if code == self.general.code:
            return self.general
        raise KeyError(code)

    def all_topics(self) -> list[Topic]:
        return [*self.topics, self.general]


def load_config(config_dir: Path | None = None) -> Config:
    config_dir = config_dir or CONFIG_DIR
    settings = _load(config_dir / "settings.yaml")
    taxonomy = _load(config_dir / "topics.yaml")

    topics = [
        Topic(
            code=t["code"],
            slug=t["slug"],
            title=t["title"],
            short=t.get("short") or t["title"],
            scope=" ".join(str(t.get("scope", "")).split()),
            strong=list(t.get("strong") or []),
            medium=list(t.get("medium") or []),
            weak=list(t.get("weak") or []),
        )
        for t in taxonomy["topics"]
    ]
    g = taxonomy["general"]
    general = Topic(
        code=g["code"],
        slug=g["slug"],
        title=g["title"],
        short=g.get("short") or g["title"],
        scope=" ".join(str(g.get("scope", "")).split()),
    )

    seen_codes = [t.code for t in topics] + [general.code]
    if len(set(seen_codes)) != len(seen_codes):
        raise ValueError("duplicate topic codes in topics.yaml")

    return Config(settings=settings, topics=topics, general=general)
