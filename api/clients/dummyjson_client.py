"""
Thin REST client wrapping DummyJSON (public demo API, no auth required).

Keeping the requests-library calls behind a client — rather than scattered
across test files — means test code reads like business intent
(``client.get_product(1)``) instead of raw HTTP plumbing, and there is one
place to add retries, headers, or auth if the target API ever needs it.
"""
from __future__ import annotations

from typing import Any

import requests

from core.config import settings


class DummyJsonClient:
    def __init__(self, base_url: str | None = None, timeout: float = 10.0):
        self.base_url = base_url or settings.api_base_url
        self.timeout = timeout
        self.session = requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def get_product(self, product_id: int) -> requests.Response:
        return self.session.get(self._url(f"/products/{product_id}"), timeout=self.timeout)

    def list_products(self, limit: int = 30, skip: int = 0) -> requests.Response:
        return self.session.get(
            self._url("/products"),
            params={"limit": limit, "skip": skip},
            timeout=self.timeout,
        )

    def search_products(self, query: str) -> requests.Response:
        return self.session.get(
            self._url("/products/search"), params={"q": query}, timeout=self.timeout
        )

    def add_product(self, payload: dict[str, Any]) -> requests.Response:
        return self.session.post(self._url("/products/add"), json=payload, timeout=self.timeout)

    def login(self, username: str, password: str) -> requests.Response:
        return self.session.post(
            self._url("/auth/login"),
            json={"username": username, "password": password},
            timeout=self.timeout,
        )
