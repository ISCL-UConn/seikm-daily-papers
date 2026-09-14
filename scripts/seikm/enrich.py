"""Optional LLM enrichment.

Off by default. The digest is fully functional without it — this adds a
one-line "why it matters to SEIKM" note per paper and a light re-rank.

To turn on:
  1. settings.yaml -> llm.enabled: true
  2. add an ANTHROPIC_API_KEY repository secret

Every failure path is soft: if the key is missing, the SDK is absent, the API
errors, or the response does not parse, the keyword digest publishes unchanged.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

log = logging.getLogger("seikm.enrich")

PROMPT = """You are assisting the ASME IDETC-CIE SEIKM technical committee \
(Systems Engineering, Information and Knowledge Management) with its daily \
scan of new arXiv preprints.

The committee's topic areas are:
{topics}

Below are {n} papers a keyword filter selected today. For each, judge how \
relevant it actually is to the committee and write one short sentence on why \
a SEIKM researcher might care. Be blunt: if a paper is only superficially \
related, say so and score it low.

Return ONLY a JSON array, one object per paper, in the same order:
[{{"i": 0, "relevance": 0-10, "why": "one sentence, max 25 words"}}]

Papers:
{papers}"""


def _client():
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        log.info("no ANTHROPIC_API_KEY; skipping LLM enrichment")
        return None
    try:
        import anthropic  # type: ignore
    except ImportError:
        log.warning("anthropic package not installed; skipping LLM enrichment")
        return None
    return anthropic.Anthropic(api_key=key)


def _extract_json(text: str) -> list[dict[str, Any]]:
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError("no JSON array in response")
    return json.loads(text[start : end + 1])


def enrich(config, papers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    cfg = config.llm
    if not cfg.get("enabled"):
        return papers
    client = _client()
    if client is None:
        return papers

    subset = papers[: int(cfg.get("max_papers", 40))]
    topics = "\n".join(f"- {t.code} {t.title}: {t.scope}" for t in config.topics)
    listing = "\n\n".join(
        f"[{i}] {p['title']}\n{' '.join((p.get('abstract') or '').split())[:700]}"
        for i, p in enumerate(subset)
    )
    prompt = PROMPT.format(topics=topics, n=len(subset), papers=listing)

    try:
        resp = client.messages.create(
            model=cfg.get("model", "claude-sonnet-4-6"),
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )
        rows = _extract_json("".join(b.text for b in resp.content if b.type == "text"))
    except Exception as exc:  # noqa: BLE001 - deliberately broad; must fail open
        if cfg.get("fail_open", True):
            log.warning("LLM enrichment failed (%s); publishing keyword digest", exc)
            return papers
        raise

    for row in rows:
        try:
            idx = int(row["i"])
            paper = subset[idx]
        except (KeyError, ValueError, IndexError):
            continue
        why = str(row.get("why", "")).strip()
        if why:
            paper["why"] = why
        if "relevance" in row:
            try:
                rel = max(0.0, min(10.0, float(row["relevance"])))
            except (TypeError, ValueError):
                continue
            paper["llm_relevance"] = rel
            base = paper.get("rank_score", paper.get("score", 0.0))
            # Blend: keyword evidence stays primary, LLM nudges by up to ~30%.
            paper["rank_score"] = round(base * (0.7 + 0.06 * rel), 3)

    log.info("LLM enrichment applied to %d papers", len(rows))
    return papers
