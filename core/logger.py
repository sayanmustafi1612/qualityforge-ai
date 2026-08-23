"""
Structured logging setup shared by UI tests, API tests, and the failure
analyzer. One call, consistent format, per-test-run log file.
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path


def get_logger(name: str, log_dir: str = "results/logs") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        # Already configured (pytest re-imports across modules)
        return logger

    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(fmt)
    logger.addHandler(console)

    Path(log_dir).mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(Path(log_dir) / "run.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger
