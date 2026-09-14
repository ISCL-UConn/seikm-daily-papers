"""Regression test for the SEIKM classifier.

Run:  python3 tests/test_classifier.py [-v]

Each fixture lists a SET of acceptable outcomes, because many real papers
legitimately straddle two SEIKM topics. The test fails if accuracy drops
below THRESHOLD, which makes it safe to keep tuning config/topics.yaml.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from seikm.classify import Classifier  # noqa: E402
from seikm.config import load_config  # noqa: E402

THRESHOLD = 0.85


def main() -> int:
    verbose = "-v" in sys.argv
    config = load_config(ROOT / "config")
    clf = Classifier(config)
    fixtures = yaml.safe_load((ROOT / "tests" / "fixtures.yaml").read_text())["papers"]

    passed, failures = 0, []
    for fx in fixtures:
        a = clf.assess(fx["title"], fx["abstract"])
        actual = a.primary if a.kept else "DROP"
        ok = actual in fx["expect"]
        passed += ok
        if not ok:
            failures.append((fx, a, actual))
        if verbose:
            flag = "ok " if ok else "FAIL"
            sec = f" +{','.join(a.secondary)}" if a.secondary else ""
            print(
                f"{flag} {actual:<10}{sec:<12} "
                f"score={a.primary_score:>6.2f} gate={a.gate_score:>6.2f}  "
                f"{fx['title'][:62]}"
            )

    total = len(fixtures)
    accuracy = passed / total
    print(f"\n{passed}/{total} acceptable  ({accuracy:.1%})")

    if failures:
        print("\nMisses:")
        for fx, a, actual in failures:
            print(f"  - {fx['title'][:70]}")
            print(f"      got {actual} (score {a.primary_score}), want one of {fx['expect']}")
            print(f"      reason: {a.reason}")
            top = sorted(
                ((c, s.score) for c, s in a.scores.items() if s.score > 0),
                key=lambda kv: kv[1],
                reverse=True,
            )[:3]
            print(f"      top scores: {top}")

    if accuracy < THRESHOLD:
        print(f"\nFAILED: accuracy {accuracy:.1%} below threshold {THRESHOLD:.0%}")
        return 1
    print(f"PASSED (threshold {THRESHOLD:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
