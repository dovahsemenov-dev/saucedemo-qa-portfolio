# QA-портфолио: автотесты UI и REST API (SauceDemo + Restful Booker)

[![tests](https://github.com/dovahsemenov-dev/saucedemo-qa-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/dovahsemenov-dev/saucedemo-qa-portfolio/actions/workflows/tests.yml)

## О проекте

Портфолио тестировщика (QA) на двух объектах тестирования:

- **UI**: учебный интернет-магазин Swag Labs / Sauce Demo — https://www.saucedemo.com
- **API**: учебный сервис бронирований Restful Booker — https://restful-booker.herokuapp.com (документация: https://restful-booker.herokuapp.com/apidoc/index.html)

Пройден полный цикл: тест-дизайн и документация, ручные проверки с баг-репортами, автотесты UI (Selenium) и API (requests + JSON-схемы), Postman-коллекция с прогоном через Newman, CI в GitHub Actions и учебные SQL-запросы.

## Что сделано

| Артефакт | Количество | Где лежит |
|---|---|---|
| Ручных тест-кейсов | 13 | [Google Таблица](https://docs.google.com/spreadsheets/d/1YnLVQ-si8GyV0SWa8AsRD8oPV4n73AlXF5m04ddiE5I/edit?gid=608250334#gid=608250334) |
| Баг-репортов | 8 (4 UI + 4 API) | [`bug-reports/`](./bug-reports/) |
| UI-автотестов | 23 | [`automation/tests/`](./automation/tests/) |
| API-автотестов | 24 | [`automation/api/`](./automation/api/) |
| Запросов в Postman-коллекции | 10 (с автопроверками) | [`api/restful_booker.postman_collection.json`](./api/restful_booker.postman_collection.json) |
| SQL-запросов | 10 | [`database/queries.sql`](./database/queries.sql) |

Последний локальный прогон: **40 passed, 7 xfailed** (xfail — воспроизводимые известные дефекты BUG-01, BUG-05…BUG-08).

## Стек

- Python 3.11+
- **UI**: Selenium 4 + pytest, Chrome, паттерн Page Object, драйвер через встроенный Selenium Manager
- **API**: pytest + requests + jsonschema (валидация ответов по JSON-схемам)
- Postman + Newman (прогон коллекции из консоли)
- pytest-html (HTML-отчёты), pytest-rerunfailures (перезапуск нестабильных UI-тестов в CI)
- GitHub Actions

## Структура репозитория

```
automation/
  api/              # API-тесты: client.py, schemas.py, фикстуры, 3 файла тестов
  pages/            # Page Object UI: base, login, inventory, cart, checkout
  tests/            # UI-тесты: логин, каталог, корзина, оформление заказа
  conftest.py       # фикстуры driver и logged_in, скриншот при падении
  config.py         # BASE_URL, таймаут (UI_TIMEOUT), пользователи стенда
api/                # Postman-коллекция Restful Booker + окружение + описание
bug-reports/        # 8 баг-репортов (BUG-01…BUG-08)
database/           # queries.sql — 10 учебных SQL-запросов
.github/workflows/  # tests.yml — CI: раздельные job ui-tests и api-tests
pytest.ini          # маркеры smoke/regression/ui/api, HTML-отчёт
requirements.txt
```

## Как запустить тесты локально

```bash
git clone https://github.com/dovahsemenov-dev/saucedemo-qa-portfolio.git
cd saucedemo-qa-portfolio

python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
pip install -r requirements.txt

pytest -m ui            # только UI-тесты (Selenium, откроется Chrome)
pytest -m api           # только API-тесты (без браузера)
pytest                  # всё вместе, отчёт в report.html
```

Headless-режим и другие варианты:

```bash
HEADLESS=1 pytest -m ui          # Linux/macOS, браузер в фоне (как в CI)
set HEADLESS=1 && pytest -m ui   # Windows (cmd)
UI_TIMEOUT=30 pytest -m ui       # увеличить таймаут ожиданий (по умолчанию 15 с)
pytest -m smoke                  # только критичные позитивные сценарии
pytest automation/tests/test_login.py -q   # один модуль
```

Прогон Postman-коллекции (нужен Node.js):

```bash
npx newman run api/restful_booker.postman_collection.json -e api/restful_booker.postman_environment.json
```

Два негативных шага коллекции (8 «неверный пароль» и 9 «неполное тело») падают намеренно: они зафиксированы как известные дефекты BUG-06 и BUG-07.

## Покрытие UI-автотестами

| Модуль | Что проверяется | Тесты |
|---|---|---|
| Авторизация | Успешный вход `standard_user` (smoke) | `test_successful_login_standard_user` |
| Авторизация | Блокировка `locked_out_user` и текст ошибки | `test_locked_out_user_sees_error` |
| Авторизация | Негативные сценарии: пустой логин, пустой пароль, неверный пароль, несуществующий пользователь + текст ошибки (параметризация) | `test_negative_login_shows_expected_error` (4 кейса) |
| Авторизация | Выход из системы через бургер-меню | `test_logout_through_menu` |
| Каталог | В каталоге 6 товаров (названия и цены) | `test_catalog_shows_six_products` |
| Каталог | Сортировка по имени A→Z и Z→A | `test_sort_by_name` (2 кейса) |
| Каталог | Сортировка по цене low→high и high→low | `test_sort_by_price` (2 кейса) |
| Каталог | Карточка товара: название и цена совпадают с каталогом | `test_product_page_matches_catalog` |
| Каталог | Известный баг BUG-01: одинаковые картинки у `problem_user` (xfail) | `test_problem_user_product_images_are_unique` |
| Корзина | Счётчик на иконке корзины = 1 (smoke) | `test_cart_badge_shows_one_after_adding_product` |
| Корзина | Добавление нескольких товаров: счётчик и состав корзины | `test_adding_several_products_updates_badge_and_cart` |
| Корзина | Удаление товара из корзины | `test_remove_product_from_cart` |
| Корзина | Корзина сохраняется после переходов между страницами | `test_cart_is_kept_after_navigation` |
| Оформление заказа | Полный e2e: логин → товар → корзина → данные → итог → «Thank you for your order!» (smoke) | `test_full_checkout_flow` |
| Оформление заказа | Валидация обязательных полей (имя, фамилия, индекс) | `test_empty_customer_fields_are_rejected` (3 кейса) |
| Оформление заказа | Item total = сумме цен, Total = Item total + Tax | `test_overview_totals_match_cart_prices` |

## Покрытие API-автотестами

Объект: Restful Booker. Каждый тест проверяет статус-код, Content-Type и — где есть тело — соответствие JSON-схеме (`automation/api/schemas.py`).

| Эндпоинт | Что проверяется | Тесты |
|---|---|---|
| POST /auth | Успешное получение токена (smoke) | `test_get_token_success` |
| POST /auth | Неверный логин/пароль и пустые креды должны давать 4xx (параметризация, xfail BUG-06) | `test_auth_with_wrong_credentials_returns_4xx` (3 кейса) |
| POST /auth | Тело ошибки — JSON; время ответа < 3 с | `test_auth_response_is_json`, `test_auth_response_time_is_fast` |
| GET /booking | Список не пустой (smoke); фильтрация по firstname и lastname | `test_get_booking_list_is_not_empty`, `test_get_booking_list_can_be_filtered` (2 кейса) |
| POST /booking | Создание: ответ по схеме, данные совпадают с отправленными (smoke) | `test_create_booking_matches_payload` |
| GET /booking/{id} | Чтение созданного бронирования (smoke); Content-Type; время ответа | `test_get_created_booking_by_id`, `test_booking_content_type_is_json`, `test_booking_response_time_is_fast` |
| PUT /booking/{id} | Полное обновление с токеном, изменения сохраняются | `test_put_booking_updates_all_fields` |
| PATCH /booking/{id} | Частичное обновление: меняется только firstname | `test_patch_booking_updates_only_firstname` |
| DELETE /booking/{id} | Удаление 201, затем GET возвращает 404 (smoke) | `test_delete_booking_then_get_returns_404` |
| Негативные | PUT/PATCH/DELETE без токена отклоняются; GET несуществующего id → 404; id не число → 404 | `test_write_methods_without_token_are_rejected` (3 кейса), `test_get_missing_booking_returns_404`, `test_get_booking_with_non_numeric_id_returns_404` |
| Негативные (xfail) | Bearer-токен (BUG-05), неполное тело POST (BUG-07), операции с несуществующим id (BUG-08) | `test_bearer_token_is_accepted`, `test_post_with_incomplete_body_returns_400`, `test_operations_on_missing_booking_return_404` |

## Известные дефекты

| ID | Серьёзность | Суть | Статус в автотестах |
|---|---|---|---|
| BUG-01 | Major | У всех товаров `problem_user` в каталоге одна картинка | xfail, UI |
| BUG-02 | Critical | `problem_user`: поле Last Name не принимает ввод при оформлении заказа | описан ручным чек-листом |
| BUG-03 | Major | `performance_glitch_user`: переход на каталог занимает 5 секунд | описан ручным чек-листом |
| BUG-04 | Major | `error_user`: некорректный расчёт Tax на экране итогов | описан ручным чек-листом |
| BUG-05 | Major | API: PUT/PATCH отклоняют заголовок `Authorization: Bearer` (403), работает только Cookie | xfail, API |
| BUG-06 | Minor | API: POST /auth возвращает 200 OK при неверных учётных данных | xfail, API + шаг 8 Postman |
| BUG-07 | Major | API: POST /booking с неполным телом возвращает 500 вместо 400 | xfail, API + шаг 9 Postman |
| BUG-08 | Minor | API: операции с несуществующим бронированием возвращают 405 вместо 404 | xfail, API |

## CI

`.github/workflows/tests.yml` запускается на push и pull request в main и состоит из двух независимых job:

- **ui-tests**: `pytest -m ui` в headless-Chrome на ubuntu-latest (Python 3.11), таймаут ожиданий 30 с (`UI_TIMEOUT`), до 2 перезапусков упавшего теста (`--reruns 2 --reruns-delay 3`), скриншот при падении встраивается в HTML-отчёт, отчёт загружается артефактом `ui-test-report`;
- **api-tests**: `pytest -m api` + прогон Postman-коллекции через Newman (Node.js 20), HTML-отчёт загружается артефактом `api-test-report`. Шаг Newman помечен `continue-on-error`, потому что шаги 8 и 9 коллекции падают на известных дефектах BUG-06 и BUG-07.

## Документация и материалы

- **Тест-дизайн**: [Google Таблица](https://docs.google.com/spreadsheets/d/1YnLVQ-si8GyV0SWa8AsRD8oPV4n73AlXF5m04ddiE5I/edit?gid=608250334#gid=608250334) — тест-план и чек-листы на 13 тест-кейсов (авторизация, каталог, корзина и оформление заказа), из них 4 связаны с UI-баг-репортами
- **Баг-репорты**: [`bug-reports/`](./bug-reports/) — BUG-01 … BUG-08 (серьёзность, приоритет, шаги воспроизведения, фактический и ожидаемый результат)
- **API**: Postman-коллекция и окружение в [`api/`](./api/), описание и команды — [`api/README.txt`](./api/README.txt); автотесты — [`automation/api/`](./automation/api/)
- **SQL**: [`database/queries.sql`](./database/queries.sql) — 10 запросов (WHERE, JOIN, GROUP BY, HAVING, подзапросы)
