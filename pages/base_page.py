"""Base class all page objects inherit from — shared waits/helpers."""
from __future__ import annotations

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, path: str = "") -> None:
        from core.config import settings

        self.page.goto(f"{settings.ui_base_url}{path}")

    def screenshot(self, name: str) -> None:
        from core.config import settings
        from pathlib import Path

        Path(settings.screenshots_dir).mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=f"{settings.screenshots_dir}/{name}.png")
