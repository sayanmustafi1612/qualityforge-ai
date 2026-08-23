"""Pydantic models used to validate API JSON shape, not just status codes."""
from __future__ import annotations

from pydantic import BaseModel


class Product(BaseModel):
    id: int
    title: str
    price: float
    stock: int
    brand: str | None = None
    category: str


class ProductList(BaseModel):
    products: list[Product]
    total: int
    skip: int
    limit: int


class LoginResponse(BaseModel):
    id: int
    username: str
    accessToken: str | None = None
    token: str | None = None
