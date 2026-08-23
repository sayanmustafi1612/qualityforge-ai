"""Page object for the post-login inventory/dashboard screen."""
from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class DashboardPage(BasePage):
    PAGE_TITLE = ".title"
    INVENTORY_ITEM = ".inventory_item"
    ADD_TO_CART_BUTTON = "button.btn_inventory"
    CART_BADGE = ".shopping_cart_badge"

    def __init__(self, page: Page):
        super().__init__(page)

    def is_loaded(self) -> bool:
        return self.page.text_content(self.PAGE_TITLE) == "Products"

    def item_count(self) -> int:
        return self.page.locator(self.INVENTORY_ITEM).count()

    def add_first_item_to_cart(self) -> None:
        self.page.locator(self.ADD_TO_CART_BUTTON).first.click()

    def cart_count(self) -> int:
        badge = self.page.locator(self.CART_BADGE)
        if badge.count() == 0:
            return 0
        return int(badge.text_content() or "0")
