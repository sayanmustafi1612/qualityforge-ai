"""
Append-only history of every test execution, in SQLite so it survives
across CI runs (commit the DB file, or persist it as a CI cache/artifact).
This is the data source for flaky-test scoring and the Streamlit dashboard.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from core.config import settings

SCHEMA = """
CREATE TABLE IF NOT EXISTS test_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_name TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('passed', 'failed', 'skipped')),
    duration_ms INTEGER NOT NULL,
    timestamp REAL NOT NULL,
    error_message TEXT
);
CREATE INDEX IF NOT EXISTS idx_test_name ON test_runs(test_name);
"""


def _connect() -> sqlite3.Connection:
    db_path = Path(settings.results_db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    return conn


def record_result(
    test_name: str,
    status: str,
    duration_ms: int,
    timestamp: float,
    error_message: str | None = None,
) -> None:
    conn = _connect()
    try:
        conn.execute(
            "INSERT INTO test_runs (test_name, status, duration_ms, timestamp, error_message) "
            "VALUES (?, ?, ?, ?, ?)",
            (test_name, status, duration_ms, timestamp, error_message),
        )
        conn.commit()
    finally:
        conn.close()


def fetch_history(limit_per_test: int | None = None) -> list[dict]:
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT test_name, status, duration_ms, timestamp, error_message "
            "FROM test_runs ORDER BY timestamp DESC"
        ).fetchall()
    finally:
        conn.close()

    cols = ["test_name", "status", "duration_ms", "timestamp", "error_message"]
    return [dict(zip(cols, row)) for row in rows]
