Материалы по тестированию REST API
==================================

Объект API-тестирования: Restful Booker (https://restful-booker.herokuapp.com)
Документация: https://restful-booker.herokuapp.com/apidoc/index.html

Это учебный стенд Sauce Labs для практики API-тестирования: CRUD-операции
над бронированиями, токенная аутентификаация, фильтрация коллекции.

Содержимое папки
----------------

1. restful_booker.postman_collection.json
   Postman-коллекция из 10 запросов. Импорт: Postman -> File -> Import.
   Сценарий по порядку: auth -> create -> get -> update -> patch -> delete
   -> get после удаления -> негативные проверки (неверный пароль, неполное тело,
   несуществующий id).
   Переменные baseUrl, token и bookingId задаются скриптами на вкладке Tests
   токен и id сохраняются из ответов.
   В каждом запросе есть автопроверки: статус-код, поля и типы тела, время
   ответа (менее 3000 мс).

2. restful_booker.postman_environment.json
   Окружение для коллекции: baseUrl, token, bookingId. Импорт вместе с коллекцией.

Запуск через Newman (Node.js 18+):
    npx newman run api/restful_booker.postman_collection.json -e api/restful_booker.postman_environment.json

Примечание: два негативных шага коллекции (8 и 9) намеренно падают — они
зафиксированы как известные дефекты BUG-06 и BUG-07, см. ../bug-reports/.

Автотесты API (pytest + requests + jsonschema) лежат в ../automation/api/.
Запуск: pytest -m api
