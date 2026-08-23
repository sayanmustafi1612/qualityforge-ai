"""
Shared fixtures. Two things worth noting:

1. `page` gives every UI test a fresh browser page and guarantees cleanup
   even on failure (via the context manager in core.driver_factory).
2. `pytest_runtest_makereport` hooks into every test result and appends a
   row to the local SQLite history DB, which `utils/failure_analyzer.py`
   later reads to compute flakiness scores. This is what lets the
   dashboard show trends across many CI runs, not just the latest one.
"""
from __future__ import annotations

import time

import pytest

from api.clients.dummyjson_client import DummyJsonClient
from core.driver_factory import new_page
from utils.results_store import record_result


@pytest.fixture
def page():
    with new_page() as p:
        yield p


@pytest.fixture
def api_client() -> DummyJsonClient:
    return DummyJsonClient()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    duration_ms = int((call.stop - call.start) * 1000)
    status = "passed" if report.passed else ("failed" if report.failed else "skipped")

    record_result(
        test_name=item.nodeid,
        status=status,
        duration_ms=duration_ms,
        timestamp=time.time(),
        error_message=str(report.longrepr) if report.failed else None,
    )
