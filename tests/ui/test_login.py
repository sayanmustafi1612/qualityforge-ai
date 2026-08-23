"""UI tests for the login flow, via the LoginPage / DashboardPage POM."""
import pytest

from core.config import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login_reaches_dashboard(page):
    login = LoginPage(page).open()
    login.login(settings.ui_username, settings.ui_password)

    dashboard = DashboardPage(page)
    assert dashboard.is_loaded()
    assert dashboard.item_count() > 0


@pytest.mark.ui
def test_invalid_login_shows_error(page):
    login = LoginPage(page).open()
    login.login("standard_user", "wrong_password")

    assert "do not match" in login.error_text().lower()


@pytest.mark.ui
def test_locked_out_user_is_blocked(page):
    login = LoginPage(page).open()
    login.login("locked_out_user", settings.ui_password)

    assert "locked out" in login.error_text().lower()
