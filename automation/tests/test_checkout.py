"""Тесты оформления заказа: e2e, валидация формы и расчёт итогов."""

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"

CUSTOMER = ("John", "Doe", "12345")


@pytest.mark.smoke
def test_full_checkout_flow(logged_in):
    inventory = InventoryPage(logged_in)
    inventory.add_to_cart(BACKPACK)
    inventory.wait_cart_count(1)

    inventory.open_cart()
    checkout = CartPage(logged_in).checkout()

    checkout.fill_customer(*CUSTOMER)
    checkout.continue_checkout().finish()

    assert checkout.confirmation_text() == "Thank you for your order!"


@pytest.mark.parametrize("fields_to_fill, expected_error", [
    ([], "First Name is required"),
    ([CheckoutPage.FIRST_NAME], "Last Name is required"),
    ([CheckoutPage.FIRST_NAME, CheckoutPage.LAST_NAME], "Postal Code is required"),
])
def test_empty_customer_fields_are_rejected(logged_in, fields_to_fill, expected_error):
    """Заполняем только первые поля: каждая итерация оставляет следующее обязательное пустым."""
    inventory = InventoryPage(logged_in)
    inventory.add_to_cart(BACKPACK)
    inventory.wait_cart_count(1)

    inventory.open_cart()
    checkout = CartPage(logged_in).checkout()
    for locator in fields_to_fill:
        checkout.fill_field(locator, "John")
    checkout.continue_checkout()

    assert checkout.error_text().endswith(expected_error)


def test_overview_totals_match_cart_prices(logged_in):
    inventory = InventoryPage(logged_in)
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    inventory.wait_cart_count(2)

    inventory.open_cart()
    cart = CartPage(logged_in)
    cart_prices = [float(p.strip("$")) for p in cart.item_prices()]

    checkout = cart.checkout()
    checkout.fill_customer(*CUSTOMER)
    checkout.continue_checkout()

    expected_subtotal = sum(cart_prices)
    assert checkout.item_total() == pytest.approx(expected_subtotal)
    assert checkout.total() == pytest.approx(checkout.item_total() + checkout.tax())
