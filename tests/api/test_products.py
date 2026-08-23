"""API tests validating both status codes and response schema/contract."""
import pytest
from pydantic import ValidationError

from api.clients.schemas import Product, ProductList


@pytest.mark.api
@pytest.mark.smoke
def test_get_single_product_schema(api_client):
    resp = api_client.get_product(1)
    assert resp.status_code == 200

    try:
        Product.model_validate(resp.json())
    except ValidationError as e:
        pytest.fail(f"Response did not match Product schema: {e}")


@pytest.mark.api
def test_list_products_pagination(api_client):
    resp = api_client.list_products(limit=10, skip=0)
    assert resp.status_code == 200

    body = ProductList.model_validate(resp.json())
    assert len(body.products) == 10
    assert body.limit == 10


@pytest.mark.api
def test_search_products_returns_matches(api_client):
    resp = api_client.search_products("phone")
    assert resp.status_code == 200

    body = resp.json()
    assert body["total"] >= 0
    for product in body["products"]:
        haystack = f"{product['title']} {product.get('description', '')}".lower()
        assert "phone" in haystack or product.get("category", "").lower() in haystack


@pytest.mark.api
@pytest.mark.regression
def test_nonexistent_product_returns_404(api_client):
    resp = api_client.get_product(999999)
    assert resp.status_code == 404
