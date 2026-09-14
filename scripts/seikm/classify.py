"""Relevance gate, veto, and SEIKM topic scoring.

Pipeline for one paper:
    1. GATE    - does this look like engineering/manufacturing/systems work at
                 all? Keeps the digest from filling up with unrelated ML.
    2. SCORE   - weighted phrase evidence per topic, with a title boost and
                 diminishing returns so one repeated phrase can't dominate.
    3. VETO    - drop semantically adjacent but out-of-scope work unless the
                 topic evidence is strong enough to override.
    4. ASSIGN  - highest-scoring topic becomes primary; runners-up become tags.
                 Anything that clears the gate but no topic threshold lands in
                 SEIKM General, which is the designed catch-all.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .config import Config, Topic
from .matcher import TextIndex


@dataclass
class TopicScore:
    code: str
    score: float
    matched: list[str] = field(default_factory=list)


@dataclass
class Assessment:
    kept: bool
    reason: str
    gate_score: float
    primary: str | None = None
    primary_score: float = 0.0
    rank_score: float = 0.0
    secondary: list[str] = field(default_factory=list)
    scores: dict[str, TopicScore] = field(default_factory=dict)
    matched_terms: list[str] = field(default_factory=list)
    vetoed_by: list[str] = field(default_factory=list)


def _decayed_sum(weights: list[float], decay: float) -> float:
    """Sum of weights, largest first, each successive one worth `decay` less."""
    total = 0.0
    for i, w in enumerate(sorted(weights, reverse=True)):
        total += w * (decay ** i)
    return total


class Classifier:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.tier_weights: dict[str, float] = config.scoring["tier_weights"]
        self.title_boost: float = float(config.scoring["title_boost"])
        self.decay: float = float(config.scoring["repeat_decay"])
        self.topic_threshold: float = float(config.scoring["topic_threshold"])
        self.secondary_threshold: float = float(config.scoring["secondary_threshold"])
        self.max_secondary: int = int(config.scoring.get("max_secondary_topics", 2))
        self.gate_reference: float = float(config.scoring.get("gate_reference", 7.0))

        gate = config.gate
        self._gate_terms: list[tuple[str, float]] = [
            *((t, self.tier_weights["strong"]) for t in gate.get("strong", [])),
            *((t, self.tier_weights["medium"]) for t in gate.get("medium", [])),
        ]
        self._gate_min: float = float(gate["min_score"])

        self._veto_terms: list[str] = list(config.veto.get("terms", []))
        self._veto_override: float = float(config.veto.get("override_topic_score", 8.0))

        self._topics: list[Topic] = config.topics

    # -- stages ------------------------------------------------------------

    def _gate_score(self, ix: TextIndex) -> float:
        weights: list[float] = []
        for term, weight in self._gate_terms:
            hit = ix.find(term)
            if hit:
                weights.append(weight * (self.title_boost if hit.in_title else 1.0))
        return _decayed_sum(weights, self.decay)

    def _score_topic(self, ix: TextIndex, topic: Topic) -> TopicScore:
        weights: list[float] = []
        matched: list[str] = []
        for term, tier in topic.tiered_terms():
            hit = ix.find(term)
            if not hit:
                continue
            weights.append(
                self.tier_weights[tier] * (self.title_boost if hit.in_title else 1.0)
            )
            matched.append(term)
        return TopicScore(
            code=topic.code,
            score=round(_decayed_sum(weights, self.decay), 3),
            matched=matched,
        )

    def _domain_factor(self, gate_score: float) -> float:
        """Down-weight papers that only just clear the relevance gate."""
        if self.gate_reference <= 0:
            return 1.0
        return min(1.0, gate_score / self.gate_reference)

    def _vetoes(self, ix: TextIndex) -> list[str]:
        return [t for t in self._veto_terms if ix.find(t)]

    # -- entry point -------------------------------------------------------

    def assess(self, title: str, abstract: str) -> Assessment:
        ix = TextIndex(title, abstract)
        gate_score = round(self._gate_score(ix), 3)

        if gate_score < self._gate_min:
            return Assessment(
                kept=False,
                reason=f"gate {gate_score} < {self._gate_min}",
                gate_score=gate_score,
            )

        scores = {t.code: self._score_topic(ix, t) for t in self._topics}
        ranked = sorted(scores.values(), key=lambda s: s.score, reverse=True)
        best = ranked[0] if ranked else None
        best_score = best.score if best else 0.0

        vetoed = self._vetoes(ix)
        if vetoed and best_score < self._veto_override:
            return Assessment(
                kept=False,
                reason=f"veto ({', '.join(vetoed[:3])}) with topic score {best_score}",
                gate_score=gate_score,
                scores=scores,
                vetoed_by=vetoed,
            )

        if best is None or best_score < self.topic_threshold:
            # Clears the gate, no named topic fits -> SEIKM General, by design.
            return Assessment(
                kept=True,
                reason="general",
                gate_score=gate_score,
                primary=self.config.general.code,
                primary_score=round(max(best_score, gate_score * 0.5), 3),
                rank_score=round(
                    max(best_score, gate_score * 0.5) * self._domain_factor(gate_score), 3
                ),
                scores=scores,
                matched_terms=sorted({m for s in scores.values() for m in s.matched})[:12],
            )

        secondary = [
            s.code
            for s in ranked[1 : 1 + self.max_secondary]
            if s.score >= self.secondary_threshold
        ]
        return Assessment(
            kept=True,
            reason="topic",
            gate_score=gate_score,
            primary=best.code,
            primary_score=best.score,
            rank_score=round(best.score * self._domain_factor(gate_score), 3),
            secondary=secondary,
            scores=scores,
            matched_terms=best.matched[:12],
        )


def assess_papers(config: Config, papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Annotate papers in place with classification results; return the keepers."""
    clf = Classifier(config)
    kept: list[dict[str, Any]] = []
    for paper in papers:
        a = clf.assess(paper.get("title", ""), paper.get("abstract", ""))
        paper["gate_score"] = a.gate_score
        paper["reason"] = a.reason
        if not a.kept:
            continue
        paper["topic"] = a.primary
        paper["score"] = a.primary_score
        paper["rank_score"] = a.rank_score
        paper["secondary_topics"] = a.secondary
        paper["matched_terms"] = a.matched_terms
        paper["topic_scores"] = {
            c: s.score for c, s in a.scores.items() if s.score > 0
        }
        kept.append(paper)
    return kept
