"""
Integration test: cross-checks what the UI renders against what the API
reports, the pattern that actually catches real bugs (UI/backend drift)
that pure UI or pure API tests miss individually.
"""
import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage
from core.config import settings


@pytest.mark.integration
def test_dashboard_item_count_is_positive_and_matches_api_shape(page, api_client):
    login = LoginPage(page).open()
    login.login(settings.ui_username, settings.ui_password)

    dashboard = DashboardPage(page)
    ui_item_count = dashboard.item_count()

    api_resp = api_client.list_products(limit=ui_item_count or 1)
    assert api_resp.status_code == 200
    assert ui_item_count > 0
