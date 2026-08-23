"""
Turns raw pass/fail history into a per-test flakiness score.

A test is "flaky" if it alternates between pass and fail across runs
without a code change — that alternation is what actually erodes trust in
a suite, more than a simple pass-rate number does. So the score below
blends two signals:

  * failure_rate      — how often it fails overall
  * transition_rate   — how often the result flips from the previous run
                         (a test that fails 100% of the time is broken,
                         not flaky; a test that flips pass/fail/pass/fail
                         is flaky)

flakiness_score = 0.5 * failure_rate + 0.5 * transition_rate, as a percentage.
"""
from __future__ import annotations

from dataclasses import dataclass

from utils.results_store import fetch_history


@dataclass
class TestHealth:
    test_name: str
    runs: int
    passed: int
    failed: int
    flakiness_score: float
    avg_duration_ms: float
    status: str  # STABLE | FLAKY | HIGH_FLAKINESS | BROKEN

    def as_dict(self) -> dict:
        return {
            "test_name": self.test_name,
            "runs": self.runs,
            "passed": self.passed,
            "failed": self.failed,
            "flakiness_score": round(self.flakiness_score, 1),
            "avg_duration_ms": round(self.avg_duration_ms, 1),
            "status": self.status,
        }


def _classify(failure_rate: float, flakiness_score: float) -> str:
    if failure_rate >= 95:
        return "BROKEN"
    if flakiness_score >= 20:
        return "HIGH_FLAKINESS"
    if flakiness_score >= 5:
        return "FLAKY"
    return "STABLE"


def compute_health(min_runs: int = 3) -> list[TestHealth]:
    history = fetch_history()

    by_test: dict[str, list[dict]] = {}
    for row in history:
        by_test.setdefault(row["test_name"], []).append(row)

    results: list[TestHealth] = []
    for test_name, rows in by_test.items():
        rows_chrono = sorted(rows, key=lambda r: r["timestamp"])
        runs = len(rows_chrono)
        passed = sum(1 for r in rows_chrono if r["status"] == "passed")
        failed = sum(1 for r in rows_chrono if r["status"] == "failed")

        if runs < min_runs:
            # Not enough data yet to call it flaky vs. just-written
            continue

        failure_rate = 100.0 * failed / runs

        transitions = sum(
            1
            for prev, curr in zip(rows_chrono, rows_chrono[1:])
            if prev["status"] != curr["status"]
        )
        transition_rate = 100.0 * transitions / max(runs - 1, 1)

        flakiness_score = 0.5 * failure_rate + 0.5 * transition_rate
        avg_duration = sum(r["duration_ms"] for r in rows_chrono) / runs

        results.append(
            TestHealth(
                test_name=test_name,
                runs=runs,
                passed=passed,
                failed=failed,
                flakiness_score=flakiness_score,
                avg_duration_ms=avg_duration,
                status=_classify(failure_rate, flakiness_score),
            )
        )

    return sorted(results, key=lambda t: t.flakiness_score, reverse=True)
