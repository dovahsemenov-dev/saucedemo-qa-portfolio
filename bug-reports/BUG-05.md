Баг-репорт BUG-05. Авторизация через заголовок Authorization: Bearer отклоняется (403 Forbidden)

Компонент: REST API Restful Booker, эндпоинты изменения данных (PUT /booking/{id}, PATCH /booking/{id})
Сервис: https://restful-booker.herokuapp.com
Серьезность: Высокая (Major)
Приоритет: Высокий (High)

Описание:
Документация API (https://restful-booker.herokuapp.com/apidoc/index.html) описывает авторизацию
для защищённых методов через заголовок Authorization со значением "Bearer <token>".
Фактически сервер отклоняет такой запрос: PUT и PATCH возвращают 403 Forbidden,
хотя токен, полученный из POST /auth, валиден. При этом те же операции проходят успешно
при авторизации через Cookie (token=<token>) и через Basic-авторизацию.

Шаги для воспроизведения:
1. Выполнить POST /auth {"username": "admin", "password": "password123"} -> получить token.
2. Выполнить POST /booking с любым валидным телом -> получить bookingid.
3. Выполнить PUT /booking/{bookingid} с заголовком Authorization: Bearer <token> и корректным телом.

Фактический результат:
403 Forbidden, тело "Forbidden". Данные не обновляются.
Проверено также: PATCH /booking/{id} с Bearer -> 403, X-Authorization: Bearer -> 403.

Ожидаемый результат:
200 OK и обновлённое бронирование в ответе, как при авторизации через Cookie.

Окружение: ОС Windows 10 Pro, Python 3.14, requests 2.34.2, стенд Heroku (Node/Express).
Автотест: automation/api/test_booking_negative.py::test_bearer_token_is_accepted
