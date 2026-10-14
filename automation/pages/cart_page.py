"""Корзина /cart.html."""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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
        """Строка товара в корзине по точному названию (ждём отрисовку списка)."""
        try:
            return self.wait.until(
                lambda _: self.card_by_name(self.ITEM, self.ITEM_NAME, name)
            )
        except TimeoutException:
            raise AssertionError(f"Товар «{name}» не найден в корзине")

    def remove(self, name):
        """Удаляет товар и ждёт, пока счётчик корзины уменьшится; иначе повторяет клик."""
        expected = self.cart_count() - 1
        for attempt in range(3):
            if self.cart_count() == expected:  # клик уже сработал, а ожидание не успело
                return
            self.item_card(name).find_element(*self.REMOVE_BUTTON).click()
            try:
                self.wait.until(lambda _: self.cart_count() == expected)
                return
            except TimeoutException:
                if attempt == 2:
                    raise

    def checkout(self):
        # Ждём адрес шага 1: на медленном стенде SPA-переход может запаздывать.
        self.click_until(self.CHECKOUT_BUTTON, EC.url_contains("checkout-step-one"))
        return CheckoutPage(self.driver)

    def continue_shopping(self):
        self.click_until(self.CONTINUE_SHOPPING, EC.url_contains("inventory.html"))
