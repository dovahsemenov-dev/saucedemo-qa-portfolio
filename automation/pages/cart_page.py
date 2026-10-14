"""Корзина /cart.html."""

from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class CartPage(BasePage):
    CART_LIST = (By.CSS_SELECTOR, "[data-test=cart-list]")
    ITEM = (By.CSS_SELECTOR, "[data-test=inventory-item]")
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test=inventory-item-name]")
    ITEM_PRICE = (By.CSS_SELECTOR, "[data-test=inventory-item-price]")
    ITEM_QUANTITY = (By.CSS_SELECTOR, "[data-test=item-quantity]")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "[data-test^='remove-']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test=checkout]")
    CONTINUE_SHOPPING = (By.CSS_SELECTOR, "[data-test=continue-shopping]")

    def open(self):
        super().open(f"{BASE_URL}/cart.html", wait_for=self.CART_LIST)
        return self

    def item_names(self):
        return self.texts(self.ITEM_NAME)

    def item_prices(self):
        return self.texts(self.ITEM_PRICE)

    def quantities(self):
        return self.texts(self.ITEM_QUANTITY)

    def item_card(self, name):
        """Строка товара в корзине по точному названию."""
        for card in self.driver.find_elements(*self.ITEM):
            if card.find_element(*self.ITEM_NAME).text == name:
                return card
        raise AssertionError(f"Товар «{name}» не найден в корзине")

    def remove(self, name):
        self.item_card(name).find_element(*self.REMOVE_BUTTON).click()

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutPage(self.driver)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING)
