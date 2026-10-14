"""Фикстуры API-тестов: клиент, токен и временное бронирование."""

import pytest

from api.client import BookingClient, booking_payload


@pytest.fixture
def client():
    return BookingClient()


@pytest.fixture
def token(client):
    response = client.auth()
    assert response.status_code == 200, f"POST /auth -> {response.status_code}: {response.text}"
    return response.json()["token"]


@pytest.fixture
def created_booking(client, token):
    """Создаёт бронирование перед тестом и удаляет его после."""
    response = client.create_booking(booking_payload())
    assert response.status_code == 200, f"POST /booking -> {response.status_code}: {response.text}"
    booking_id = response.json()["bookingid"]

    yield booking_id

    client.delete_booking(booking_id, token)
