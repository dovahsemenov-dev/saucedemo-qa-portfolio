"""Клиент REST API Restful Booker: базовый URL, сессия и методы эндпоинтов."""

import requests

BASE_URL = "https://restful-booker.herokuapp.com"

# Учётные данные стенда из документации: https://restful-booker.herokuapp.com/apidoc/index.html
USERNAME = "admin"
PASSWORD = "password123"


class BookingClient:
    """Тонкая обёртка над requests.Session с методами каждого эндпоинта."""

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    @staticmethod
    def auth_headers(token):
        """Авторизация для PUT/PATCH/DELETE.

        На стенде заголовок Authorization: Bearer отклоняется (см. bug-reports/BUG-05.md),
        поэтому используется рабочий вариант — Cookie.
        """
        return {"Cookie": f"token={token}"}

    def auth(self, username=USERNAME, password=PASSWORD):
        return self.session.post(f"{self.base_url}/auth",
                                 json={"username": username, "password": password}, timeout=15)

    def get_bookings(self, **params):
        return self.session.get(f"{self.base_url}/booking", params=params, timeout=15)

    def get_booking(self, booking_id):
        return self.session.get(f"{self.base_url}/booking/{booking_id}", timeout=15)

    def create_booking(self, payload):
        return self.session.post(f"{self.base_url}/booking", json=payload, timeout=15)

    def update_booking(self, booking_id, payload, token=None):
        return self.session.put(f"{self.base_url}/booking/{booking_id}", json=payload,
                                headers=self.auth_headers(token), timeout=15)

    def patch_booking(self, booking_id, payload, token=None):
        return self.session.patch(f"{self.base_url}/booking/{booking_id}", json=payload,
                                  headers=self.auth_headers(token), timeout=15)

    def delete_booking(self, booking_id, token=None):
        return self.session.delete(f"{self.base_url}/booking/{booking_id}",
                                   headers=self.auth_headers(token), timeout=15)


# Типовое тело бронирования — используется в тестах и фикстурах.
def booking_payload(**overrides):
    payload = {
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2018-01-01", "checkout": "2019-01-01"},
        "additionalneeds": "Breakfast",
    }
    payload.update(overrides)
    return payload
