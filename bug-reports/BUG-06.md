Баг-репорт BUG-06. POST /auth возвращает 200 OK при неверных учётных данных

Компонент: REST API Restful Booker, аутентификация (POST /auth)
Сервис: https://restful-booker.herokuapp.com
Серьезность: Средняя (Minor)
Приоритет: Средний (Medium)

Описание:
При отправке POST /auth с неверным паролем сервер отвечает кодом 200 OK с телом
{"reason":"Bad credentials"} вместо ошибки аутентификации (401 Unauthorized).
Клиент, ориентирующийся только на код ответа, сочтёт попытку входа успешной.
Та же проблема при пустом теле и пустом пароле.

Шаги для воспроизведения:
1. Выполнить POST /auth с телом {"username": "admin", "password": "wrong"}.
2. Проверить статус-код ответа.

Фактический результат:
200 OK, тело {"reason":"Bad credentials"}. Повторяется для пустого пароля и пустого тела.

Ожидаемый результат:
401 Unauthorized (или 400 Bad Request для пустого тела) — любой 4xx-код,
сигнализирующий об отклонённой аутентификации.

Окружение: ОС Windows 10 Pro, Python 3.14, requests 2.34.2, стенд Heroku (Node/Express).
Автотест: automation/api/test_auth.py::test_auth_with_wrong_credentials_returns_4xx
