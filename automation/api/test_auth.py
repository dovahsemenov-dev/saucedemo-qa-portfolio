"""API-тесты аутентификации POST /auth."""

import pytest

from api import schemas
from api.client import USERNAME, BookingClient
from api.schemas import validate

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.smoke
def test_get_token_success(client):
    response = client.auth()

    token = validate(response, schemas.AUTH_TOKEN)
    assert len(token["token"]) > 0


@pytest.mark.parametrize("username, password", [
    (USERNAME, "wrong_password"),
    ("wrong_user", "password123"),
    ("", ""),
])
@pytest.mark.xfail(
    reason="Известный дефект BUG-06: неверные учётные данные возвращают 200 OK, "
           "см. bug-reports/BUG-06.md",
    strict=False,
)
def test_auth_with_wrong_credentials_returns_4xx(client, username, password):
    response = client.auth(username, password)

    assert response.status_code in (400, 401, 403)


def test_auth_response_is_json(client):
    response = client.auth(USERNAME, "wrong_password")

    # Тело с сообщением об ошибке есть, но статус пока не сигнализирует об ошибке (BUG-06).
    assert response.headers["Content-Type"].startswith("application/json")
    assert "reason" in response.json()


def test_auth_response_time_is_fast(client):
    """Мягкая проверка производительности: ответ быстрее 3 секунд."""
    response = client.auth()

    assert response.elapsed.total_seconds() < 3
