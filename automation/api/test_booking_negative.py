"""Негативные API-тесты: отсутствие токена, несуществующие id, некорректные тела."""

import pytest

from api.client import booking_payload

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.parametrize("method", ["update", "patch", "delete"])
def test_write_methods_without_token_are_rejected(client, created_booking, method):
    payload = booking_payload()
    call = {
        "update": lambda: client.update_booking(created_booking, payload),
        "patch": lambda: client.patch_booking(created_booking, {"firstname": "Anon"}),
        "delete": lambda: client.delete_booking(created_booking),
    }[method]

    response = call()

    assert response.status_code in (401, 403)


def test_get_missing_booking_returns_404(client):
    response = client.get_booking(999999)

    assert response.status_code == 404


@pytest.mark.xfail(
    reason="Известный дефект BUG-05: PUT/PATCH отклоняют Authorization: Bearer, "
           "см. bug-reports/BUG-05.md",
    strict=False,
)
def test_bearer_token_is_accepted(client, created_booking):
    payload = booking_payload(firstname="Bearer")
    response = client.session.put(
        f"{client.base_url}/booking/{created_booking}",
        json=payload,
        headers={"Authorization": f"Bearer {client.auth().json()['token']}"},
        timeout=15,
    )

    assert response.status_code == 200


@pytest.mark.xfail(
    reason="Известный дефект BUG-07: неполное тело POST /booking даёт 500 вместо 400, "
           "см. bug-reports/BUG-07.md",
    strict=False,
)
def test_post_with_incomplete_body_returns_400(client):
    response = client.create_booking({"firstname": "OnlyName"})

    assert response.status_code == 400


@pytest.mark.xfail(
    reason="Известный дефект BUG-08: операции с несуществующим бронированием дают 405 "
           "вместо 404, см. bug-reports/BUG-08.md",
    strict=False,
)
def test_operations_on_missing_booking_return_404(client, token):
    # GET корректно отдаёт 404, а PUT/DELETE — 405; проверяем DELETE на несуществующем id.
    response = client.delete_booking(999999, token)

    assert response.status_code == 404


def test_get_booking_with_non_numeric_id_returns_404(client):
    response = client.get_booking("abc")

    assert response.status_code == 404
