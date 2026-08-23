"""API tests for the auth/login contract."""
import pytest

from api.clients.schemas import LoginResponse


@pytest.mark.api
def test_login_with_valid_credentials(api_client):
    resp = api_client.login("emilys", "emilyspass")
    assert resp.status_code == 200
    LoginResponse.model_validate(resp.json())


@pytest.mark.api
@pytest.mark.regression
def test_login_with_invalid_credentials_is_rejected(api_client):
    resp = api_client.login("emilys", "wrong-password")
    assert resp.status_code in (400, 401)
