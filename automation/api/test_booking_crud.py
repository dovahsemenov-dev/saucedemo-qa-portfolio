"""API-тесты основного сценария: создание, чтение, обновление, удаление."""

import pytest

from api import schemas
from api.client import booking_payload
from api.schemas import validate

pytestmark = [pytest.mark.api, pytest.mark.regression]


@pytest.mark.smoke
def test_get_booking_list_is_not_empty(client):
    response = client.get_bookings()

    bookings = validate(response, schemas.BOOKING_LIST)
    assert len(bookings) > 0


@pytest.mark.parametrize("filter_param", ["firstname", "lastname"])
def test_get_booking_list_can_be_filtered(client, filter_param):
    # Имя из документации стенда: у бронирования Susan Jackson есть и firstname, и lastname.
    response = client.get_bookings(**{filter_param: "Susan"})

    validate(response, schemas.BOOKING_LIST)


@pytest.mark.smoke
def test_create_booking_matches_payload(client):
    payload = booking_payload()

    response = client.create_booking(payload)

    body = validate(response, schemas.CREATED_BOOKING)
    assert body["booking"] == payload


@pytest.mark.smoke
def test_get_created_booking_by_id(client, token):
    payload = booking_payload(firstname="Created", lastname="Fixture")
    booking_id = client.create_booking(payload).json()["bookingid"]

    response = client.get_booking(booking_id)
    body = validate(response, schemas.BOOKING)

    assert body == payload

    client.delete_booking(booking_id, token)


def test_put_booking_updates_all_fields(client, created_booking, token):
    payload = booking_payload(firstname="Updated", lastname="Person", totalprice=300,
                              depositpaid=False,
                              bookingdates={"checkin": "2025-02-01", "checkout": "2025-02-03"},
                              additionalneeds="Pizza")

    response = client.update_booking(created_booking, payload, token)

    body = validate(response, schemas.BOOKING)
    assert body == payload

    stored = validate(client.get_booking(created_booking), schemas.BOOKING)
    assert stored == payload


def test_patch_booking_updates_only_firstname(client, created_booking, token):
    original = validate(client.get_booking(created_booking), schemas.BOOKING)

    response = client.patch_booking(created_booking, {"firstname": "Patched"}, token)

    body = validate(response, schemas.BOOKING)
    assert body["firstname"] == "Patched"
    assert body["lastname"] == original["lastname"]
    assert body["totalprice"] == original["totalprice"]


@pytest.mark.smoke
def test_delete_booking_then_get_returns_404(client, token):
    created = client.create_booking(booking_payload()).json()["bookingid"]

    delete = client.delete_booking(created, token)
    assert delete.status_code == 201

    # После удаления ресурс недоступен. Повторный DELETE даёт 405 — дефект BUG-08.
    assert client.get_booking(created).status_code == 404


def test_booking_content_type_is_json(client, created_booking):
    response = client.get_booking(created_booking)

    assert response.headers["Content-Type"].startswith("application/json")


def test_booking_response_time_is_fast(client, created_booking):
    """Мягкая проверка производительности: ответ быстрее 3 секунд."""
    response = client.get_booking(created_booking)

    assert response.elapsed.total_seconds() < 3
