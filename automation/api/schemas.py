"""JSON-схемы ответов API Restful Booker и их валидация через jsonschema."""

import jsonschema

BOOKING_DATES = {
    "type": "object",
    "properties": {
        "checkin": {"type": "string", "format": "date"},
        "checkout": {"type": "string", "format": "date"},
    },
    "required": ["checkin", "checkout"],
}

# Ответ POST /booking и GET /booking/{id}
BOOKING = {
    "type": "object",
    "properties": {
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "totalprice": {"type": "integer"},
        "depositpaid": {"type": "boolean"},
        "bookingdates": BOOKING_DATES,
        "additionalneeds": {"type": "string"},
    },
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
}

# Ответ POST /booking дополнительно оборачивает бронирование в id
CREATED_BOOKING = {
    "type": "object",
    "properties": {
        "bookingid": {"type": "integer"},
        "booking": BOOKING,
    },
    "required": ["bookingid", "booking"],
}

# Ответ POST /auth
AUTH_TOKEN = {
    "type": "object",
    "properties": {"token": {"type": "string", "minLength": 1}},
    "required": ["token"],
}

# Элемент списка GET /booking
BOOKING_LIST_ITEM = {
    "type": "object",
    "properties": {"bookingid": {"type": "integer"}},
    "required": ["bookingid"],
}

BOOKING_LIST = {"type": "array", "items": BOOKING_LIST_ITEM}


def validate(response, schema, expected_status=200):
    """Проверяет статус-код, Content-Type и соответствие тела JSON-схеме."""
    assert response.status_code == expected_status, \
        f"Ожидался {expected_status}, получен {response.status_code}: {response.text}"
    assert response.headers["Content-Type"].startswith("application/json"), \
        f"Неожиданный Content-Type: {response.headers.get('Content-Type')}"
    jsonschema.validate(response.json(), schema)
    return response.json()
