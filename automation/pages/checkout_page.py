"""Оформление заказа: шаг 1 (данные), шаг 2 (итог) и финальный экран."""

from selenium.webdriver.common.by import By

from config import BASE_URL
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test=firstName]")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test=lastName]")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test=postalCode]")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-test=continue]")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "[data-test=cancel]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test=error]")

    # Шаг 2 — Checkout: Overview
    ITEM_NAME = (By.CSS_SELECTOR, "[data-test=inventory-item-name]")
    ITEM_PRICE = (By.CSS_SELECTOR, "[data-test=inventory-item-price]")
    ITEM_TOTAL = (By.CSS_SELECTOR, "[data-test=subtotal-label]")
    TAX = (By.CSS_SELECTOR, "[data-test=tax-label]")
    TOTAL = (By.CSS_SELECTOR, "[data-test=total-label]")
    FINISH_BUTTON = (By.CSS_SELECTOR, "[data-test=finish]")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test=complete-header]")

    def open(self):
        super().open(f"{BASE_URL}/checkout-step-one.html", wait_for=self.FIRST_NAME)
        return self

    def fill_customer(self, first_name, last_name, postal_code):
        """Заполняет форму данных покупателя (шаг 1)."""
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        return self

    def fill_field(self, locator, value):
        """Заполняет одно поле — удобно для проверки валидации по одному полю."""
        self.type(locator, value)
        return self

    def continue_checkout(self):
        self.click(self.CONTINUE_BUTTON)
        return self

    def error_text(self):
        return self.text(self.ERROR_MESSAGE)

    def item_names(self):
        return self.texts(self.ITEM_NAME)

    def item_prices(self):
        return self.texts(self.ITEM_PRICE)

    @staticmethod
    def _money(text):
        """'Item total: $29.99' -> 29.99"""
        return float(text.split("$")[1])

    def item_total(self):
        return self._money(self.text(self.ITEM_TOTAL))

    def tax(self):
        return self._money(self.text(self.TAX))

    def total(self):
        return self._money(self.text(self.TOTAL))

    def finish(self):
        self.click(self.FINISH_BUTTON)
        return self

    def confirmation_text(self):
        return self.text(self.COMPLETE_HEADER)

    def cancel(self):
        self.click(self.CANCEL_BUTTON)
