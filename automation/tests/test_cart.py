"""Тесты корзины: счётчик, состав, удаление и сохранение между переходами."""

import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.ui


BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"
ONESIE = "Sauce Labs Onesie"

@pytest.mark.smoke
def test_cart_badge_shows_one_after_adding_product(logged_in):
    inventory = InventoryPage(logged_in)

    inventory.add_to_cart(BACKPACK)
    inventory.wait_cart_count(1)

    assert inventory.cart_count() == 1

def test_adding_several_products_updates_badge_and_cart(logged_in):
    inventory = InventoryPage(logged_in)
    expected = sorted([BACKPACK, BIKE_LIGHT, ONESIE])

    for name in [BACKPACK, BIKE_LIGHT, ONESIE]:
        inventory.add_to_cart(name)
    inventory.wait_cart_count(3)

    inventory.open_cart()
    cart = CartPage(logged_in)

    assert inventory.cart_count() == 3
    assert sorted(cart.item_names()) == expected
    assert cart.quantities() == ["1", "1", "1"]

def test_remove_product_from_cart(logged_in):
    inventory = InventoryPage(logged_in)
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    inventory.wait_cart_count(2)

    inventory.open_cart()
    cart = CartPage(logged_in)
    cart.remove(BACKPACK)
    cart.wait_cart_count(1)

    assert cart.item_names() == [BIKE_LIGHT]
    assert cart.cart_count() == 1

def test_cart_is_kept_after_navigation(logged_in):
    inventory = InventoryPage(logged_in)
    inventory.add_to_cart(BACKPACK)
    inventory.wait_cart_count(1)

    inventory.open_cart()
    cart = CartPage(logged_in)
    assert cart.item_names() == [BACKPACK]

    cart.continue_shopping()
    assert inventory.cart_count() == 1

    inventory.open_cart()
    assert CartPage(logged_in).item_names() == [BACKPACK]
    assert inventory.cart_count() == 1
