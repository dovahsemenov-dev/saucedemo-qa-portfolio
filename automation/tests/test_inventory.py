"""Тесты каталога: количество товаров, сортировки и карточка товара."""

import pytest

from config import PASSWORD, PROBLEM_USER
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

BACKPACK = "Sauce Labs Backpack"

# Значения по умолчанию и ожидаемый порядок для каждой сортировки.
NAME_SORTS = [("az", False), ("za", True)]
PRICE_SORTS = [("lohi", False), ("hilo", True)]


def test_catalog_shows_six_products(logged_in):
    page = InventoryPage(logged_in)

    assert len(page.product_names()) == 6
    assert len(page.product_prices()) == 6


@pytest.mark.parametrize("sort_value, reverse", NAME_SORTS)
def test_sort_by_name(logged_in, sort_value, reverse):
    page = InventoryPage(logged_in)
    expected = sorted(page.product_names(), reverse=reverse)

    page.sort_by(sort_value)
    page.wait_product_names(expected)

    assert page.product_names() == expected


@pytest.mark.parametrize("sort_value, reverse", PRICE_SORTS)
def test_sort_by_price(logged_in, sort_value, reverse):
    page = InventoryPage(logged_in)
    # Цены берём в текущем порядке, чтобы сравнение не зависело от порядка имён.
    prices = [float(p.strip("$")) for p in page.product_prices()]
    expected_prices = sorted(prices, reverse=reverse)

    page.sort_by(sort_value)
    page.wait_product_prices([f"${p:.2f}" for p in expected_prices])

    assert [float(p.strip("$")) for p in page.product_prices()] == pytest.approx(expected_prices)


def test_product_page_matches_catalog(logged_in):
    page = InventoryPage(logged_in)
    catalog_price = page.product_price(BACKPACK)

    page.open_product(BACKPACK)

    assert page.detail_name() == BACKPACK
    assert page.detail_price() == catalog_price

    page.back_to_products()
    page.wait.until(lambda _: len(page.product_names()) == 6)
    assert len(page.product_names()) == 6


@pytest.mark.xfail(
    reason="Известный дефект BUG-01: у всех товаров problem_user одно и то же изображение, "
           "см. bug-reports/BUG-01.md",
    strict=False,
)
def test_problem_user_product_images_are_unique(driver):
    LoginPage(driver).open().login(PROBLEM_USER, PASSWORD)
    images = InventoryPage(driver).product_images()

    assert len(set(images)) == 6, "Каждый товар должен иметь своё изображение"
