"""UI tests for the add-to-cart flow, building on the login fixture flow."""
import pytest

from core.config import settings
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


@pytest.fixture
def logged_in_dashboard(page):
    login = LoginPage(page).open()
    login.login(settings.ui_username, settings.ui_password)
    return DashboardPage(page)


@pytest.mark.ui
def test_add_item_updates_cart_badge(logged_in_dashboard):
    logged_in_dashboard.add_first_item_to_cart()
    assert logged_in_dashboard.cart_count() == 1


@pytest.mark.ui
@pytest.mark.regression
def test_cart_starts_empty(logged_in_dashboard):
    assert logged_in_dashboard.cart_count() == 0
