"""
Centralized configuration for QualityForge AI.

All environment-dependent values live here, loaded from environment
variables with sane local defaults. Never hardcode URLs/creds in tests.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


def _env(key: str, default: str) -> str:
    return os.environ.get(key, default)


@dataclass(frozen=True)
class Settings:
    # UI target under test (swap for your own app; SauceDemo used as a
    # public, stable demo site so the framework is runnable out of the box)
    ui_base_url: str = _env("QF_UI_BASE_URL", "https://www.saucedemo.com")
    ui_username: str = _env("QF_UI_USERNAME", "standard_user")
    ui_password: str = _env("QF_UI_PASSWORD", "secret_sauce")

    # API target under test (public demo REST API, no auth required)
    api_base_url: str = _env("QF_API_BASE_URL", "https://dummyjson.com")

    # Playwright
    browser: str = _env("QF_BROWSER", "chromium")  # chromium | firefox | webkit
    headless: bool = _env("QF_HEADLESS", "true").lower() == "true"
    slow_mo_ms: int = int(_env("QF_SLOW_MO_MS", "0"))
    default_timeout_ms: int = int(_env("QF_TIMEOUT_MS", "10000"))

    # Retry / execution
    max_retries: int = int(_env("QF_MAX_RETRIES", "2"))

    # Storage
    results_db_path: str = _env("QF_RESULTS_DB", "results/history.db")
    screenshots_dir: str = _env("QF_SCREENSHOTS_DIR", "results/screenshots")


settings = Settings()
