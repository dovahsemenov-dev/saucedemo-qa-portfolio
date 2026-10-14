# QA-портфолио: автотесты для интернет-магазина Swag Labs (Sauce Demo)

[![tests](https://github.com/dovahsemenov-dev/saucedemo-qa-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/dovahsemenov-dev/saucedemo-qa-portfolio/actions/workflows/tests.yml)

## О проекте

Проект демонстрирует навыки тестировщика (QA) на реальном стенде: учебном интернет-магазине **Swag Labs / Sauce Demo** — https://www.saucedemo.com.

Сделан полный цикл проверок: тест-дизайн и тест-документация, ручные проверки с баг-репортами, тестирование API-коллекцией в Postman, учебные SQL-запросы и **UI-автотесты на Selenium 4 + pytest** с запуском в CI.

## Что сделано

| Артефакт | Количество | Где лежит |
|---|---|---|
| Ручных тест-кейсов (чек-листы) | 13 | [Google Таблица](https://docs.google.com/spreadsheets/d/1YnLVQ-si8GyV0SWa8AsRD8oPV4n73AlXF5m04ddiE5I/edit?gid=608250334#gid=608250334) |
| Баг-репортов | 4 | [`bug-reports/`](./bug-reports/) |
| UI-автотестов | 23 (в т.ч. 3 smoke, 1 xfail на известный баг) | [`automation/tests/`](./automation/tests/) |
| Запросов в Postman-коллекции | 3 | [`saucedemo_api_collection.json`](./saucedemo_api_collection.json) |
| SQL-запросов | 10 | [`database/queries.sql`](./database/queries.sql) |

Последний прогон локально: **22 passed, 1 xfailed** (xfail — воспроизводимый известный дефект BUG-01).

## Стек

- Python 3.11+
- pytest + pytest-html (HTML-отчёт со скриншотами при падении)
- Selenium 4, Chrome (драйвер поднимается встроенным **Selenium Manager**, `webdriver-manager` не используется)
- GitHub Actions (CI)
- Postman — проверка API-сценариев
- SQL — учебные запросы

## Структура репозитория

```
automation/
  pages/            # Page Object: base, login, inventory, cart, checkout
  tests/            # автотесты: логин, каталог, корзина, оформление заказа
  conftest.py       # фикстуры driver и logged_in, скриншот при падении
  config.py         # BASE_URL, пользователи, пароль
bug-reports/        # 4 оформленных баг-репорта
api/                # описание Postman-коллекции
database/           # queries.sql — 10 учебных SQL-запросов
.github/workflows/  # tests.yml — CI-запуск тестов
saucedemo_api_collection.json  # коллекция Postman
pytest.ini          # маркеры smoke/regression, путь к тестам, HTML-отчёт
requirements.txt
```

## Как запустить тесты локально

```bash
# 1. Клонировать репозиторий и перейти в него
git clone https://github.com/dovahsemenov-dev/saucedemo-qa-portfolio.git
cd saucedemo-qa-portfolio

# 2. Создать виртуальное окружение и установить зависимости
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
pip install -r requirements.txt

# 3. Запустить тесты (браузер откроется в окне)
pytest

# headless-режим (как в CI)
HEADLESS=1 pytest                # Linux/macOS
set HEADLESS=1 && pytest         # Windows (cmd)
```

HTML-отчёт сохраняется в `report.html` (открывается в браузере, при падении теста к нему прикрепляется скриншот).

Полезные варианты запуска:

```bash
pytest -m smoke          # только критичные позитивные сценарии
pytest -m regression     # полный регрессионный набор
pytest automation/tests/test_login.py -q   # один модуль
```

## Покрытие автотестами

| Модуль | Что проверяется | Тесты |
|---|---|---|
| Авторизация | Успешный вход `standard_user` (smoke) | `test_login.py::test_successful_login_standard_user` |
| Авторизация | Блокировка `locked_out_user` и текст ошибки | `test_locked_out_user_sees_error` |
| Авторизация | Негативные сценарии (пустой логин, пустой пароль, неверный пароль, несуществующий пользователь) + текст ошибки — параметризация | `test_negative_login_shows_expected_error` (4 кейса) |
| Авторизация | Выход из системы через бургер-меню | `test_logout_through_menu` |
| Каталог | В каталоге 6 товаров (названия и цены) | `test_catalog_shows_six_products` |
| Каталог | Сортировка по имени A→Z и Z→A | `test_sort_by_name` (2 кейса) |
| Каталог | Сортировка по цене low→high и high→low | `test_sort_by_price` (2 кейса) |
| Каталог | Карточка товара: название и цена совпадают с каталогом, возврат в каталог | `test_product_page_matches_catalog` |
| Каталог | Известный баг BUG-01: одинаковые картинки у `problem_user` | `test_problem_user_product_images_are_unique` (xfail) |
| Корзина | Счётчик на иконке корзины = 1 (smoke) | `test_cart_badge_shows_one_after_adding_product` |
| Корзина | Добавление нескольких товаров: счётчик и состав корзины | `test_adding_several_products_updates_badge_and_cart` |
| Корзина | Удаление товара из корзины | `test_remove_product_from_cart` |
| Корзина | Корзина сохраняется после переходов между страницами | `test_cart_is_kept_after_navigation` |
| Оформление заказа | Полный e2e: логин → товар → корзина → данные → итог → «Thank you for your order!» (smoke) | `test_full_checkout_flow` |
| Оформление заказа | Валидация обязательных полей формы (имя, фамилия, индекс) | `test_empty_customer_fields_are_rejected` (3 кейса) |
| Оформление заказа | Item total = сумме цен, Total = Item total + Tax | `test_overview_totals_match_cart_prices` |

Итого: 23 тест-кейса в сьюте (20 функций, 3 из них параметризованы).

## Документация и материалы

- **Тест-дизайн** (тест-план, чек-листы и тест-кейсы): [Google Таблица](https://docs.google.com/spreadsheets/d/1YnLVQ-si8GyV0SWa8AsRD8oPV4n73AlXF5m04ddiE5I/edit?gid=608250334#gid=608250334) — 13 тест-кейсов, из них 4 связаны с баг-репортами
- **Баг-репорты**: [`bug-reports/`](./bug-reports/) — BUG-01 … BUG-04 (severity/priority, шаги воспроизведения, фактический и ожидаемый результат)
- **API**: [`saucedemo_api_collection.json`](./saucedemo_api_collection.json) и описание в [`api/README.txt`](./api/README.txt)
- **SQL**: [`database/queries.sql`](./database/queries.sql) — 10 запросов (WHERE, JOIN, GROUP BY, HAVING, подзапросы)

## Известные дефекты

Автотест `test_problem_user_product_images_are_unique` помечен `@pytest.mark.xfail` и падает намеренно: он фиксирует открытый баг **BUG-01** (у всех товаров `problem_user` одинаковая картинка). Остальные баг-репорты (BUG-02, BUG-03, BUG-04) описаны в [`bug-reports/`](./bug-reports/) и покрыты ручными чек-листами.
