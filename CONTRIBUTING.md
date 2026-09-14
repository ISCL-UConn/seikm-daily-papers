# Contributing

The most useful contribution is **telling the classifier it got something
wrong**. It reads only titles and abstracts, so it will mis-file papers. Every
correction makes the digest better for the whole committee.

## Fixing a mis-filed paper

Almost every fix is a one-line change to [`config/topics.yaml`](config/topics.yaml).

**A paper landed in the wrong topic.** Find a phrase that distinguishes the
correct topic and add it to that topic's `strong` list:

```yaml
  - code: SEIKM-04
    ...
    strong:
      - takt time          # <- add this line
```

**A paper landed in SEIKM General but belongs somewhere named.** Same fix: the
paper matched no topic strongly enough. Add the phrase that should have caught
it. A single `strong` phrase is enough to clear the topic threshold.

**Irrelevant papers keep appearing.** Two levers, in order of preference:

1. Add a distinguishing phrase to `veto.terms` in
   [`config/settings.yaml`](config/settings.yaml) — targeted, and it won't
   affect anything else.
2. Raise `gate.min_score` — blunt, and it will quietly drop good papers too.
   Check the effect with `--dry-run` before proposing it.

**A whole area is missing.** Add its vocabulary to the closest topic, or open an
issue proposing a new one. Empty topics and an overflowing SEIKM General are
both useful signals for the 2027 track structure — please raise them rather
than silently patching around them.

## Before you open the pull request

```bash
pip install -r requirements.txt
python3 tests/test_classifier.py -v     # must stay above the 85% threshold
```

The test set is [`tests/fixtures.yaml`](tests/fixtures.yaml): 45 real arXiv
papers, each labelled with the set of topics that would be a defensible home
(many legitimately straddle two). CI runs this on every pull request touching
`config/`, `scripts/` or `tests/`.

If your change makes the test fail, that is the test doing its job — it means
widening one topic pulled papers out of another. Either narrow the phrase, or,
if the new behaviour is genuinely better, update the affected fixture's `expect`
list in the same pull request and say why in the description.

**Adding fixtures is welcome.** A paper the classifier handled badly, added to
`fixtures.yaml` with the right answer, permanently prevents that regression.

## Changing the schedule or sources

`config/settings.yaml` holds the arXiv categories and the display caps. The cron
schedule is in [`.github/workflows/daily.yml`](.github/workflows/daily.yml).

Adding a category to `harvest.rss_categories` is cheap — categories are batched
into a handful of feed requests, and the relevance gate filters the extra volume
locally. That is the right way to widen coverage.

Do not switch `harvest.source` to `api` for the scheduled run. arXiv's search
API returns HTTP 429 to shared cloud IP ranges, and every GitHub Actions runner
is in one; the API path exists for local backfill
(`--source api --lookback 7`), where your own IP is doing the asking.

## Turning on LLM scoring

Off by default so the digest runs with no secrets and no cost. To enable:

1. Set `llm.enabled: true` in `config/settings.yaml`.
2. Uncomment `anthropic` in `requirements.txt`.
3. Add an `ANTHROPIC_API_KEY` repository secret.

Each paper then gets a one-line "why it matters to SEIKM" note, and the ranking
blends keyword evidence with the model's relevance judgment. Keyword evidence
stays primary. If the key is missing or the call fails, the run publishes the
keyword digest unchanged rather than failing.
