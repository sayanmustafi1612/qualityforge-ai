"""
Owns Playwright browser/context/page lifecycle so tests never touch
Playwright bootstrapping directly. Keeps browser choice, headless mode,
timeouts, and video/trace capture in one place.
"""
from __future__ import annotations

from contextlib import contextmanager
context_kwargs: dict[str, Any] = {}

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from core.config import settings


@contextmanager
def new_page(record_video: bool = False, trace: bool = False) -> Iterator[Page]:
    """Yield a ready-to-use Page with sane defaults, and always clean up."""
    with sync_playwright() as pw:
        browser_type = getattr(pw, settings.browser)
        browser: Browser = browser_type.launch(
            headless=settings.headless,
            slow_mo=settings.slow_mo_ms,
        )

        context_kwargs: dict[str, str] = {}
        if record_video:
            context_kwargs["record_video_dir"] = "results/videos"

        context: BrowserContext = browser.new_context(**context_kwargs)
        context.set_default_timeout(settings.default_timeout_ms)

        if trace:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()
        try:
            yield page
        finally:
            if trace:
                context.tracing.stop(path="results/traces/trace.zip")
            context.close()
            browser.close()
