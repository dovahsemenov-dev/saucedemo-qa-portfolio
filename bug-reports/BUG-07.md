Баг-репорт BUG-07. POST /booking с неполным телом возвращает 500 Internal Server Error

Компонент: REST API Restful Booker, создание бронирования (POST /booking)
Сервис: https://restful-booker.herokuapp.com
Серьезность: Высокая (Major)
Приоритет: Высокий (High)

Описание:
Запрос POST /booking с отсутствующими обязательными полями (например, только firstname)
приводит к необработанной ошибке сервера: ответ 500 Internal Server Error с пустым телом
"text/plain". Ошибки валидации входных данных должны возвращаться как 400 Bad Request
с описанием проблемы, а не как внутренняя ошибка сервера.

Шаги для воспроизведения:
1. Выполнить POST /booking с телом {"firstname": "OnlyName"} и заголовком Content-Type: application/json.

Фактический результат:
500 Internal Server Error, тело "Internal Server Error" (text/plain).

Ожидаемый результат:
400 Bad Request с описанием некорректного тела запроса.

Окружение: ОС Windows 10 Pro, Python 3.14, requests 2.34.2, стенд Heroku (Node/Express).
Автотест: automation/api/test_booking_negative.py::test_post_with_incomplete_body_returns_400
