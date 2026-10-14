"""Каталог товаров /inventory.html и карточка товара /inventory-item.html."""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from config import BASE_URL
from pages.base_page import BasePage


class InventoryPage(BasePage):
    PRODUCT_LIST = (By.CSS_SELECTOR, "[data-test=inventory-item]")
    PRODUCT_NAME = (By.CSS_SELECTOR, "[data-test=inventory-item-name]")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "[data-test=inventory-item-price]")
    # data-test картинки имеет вид inventory-item-<slug>-img
    PRODUCT_IMAGE = (By.CSS_SELECTOR, "[data-test^='inventory-item-'][data-test$='-img']")
    SORT_SELECT = (By.CSS_SELECTOR, "[data-test=product-sort-container]")
    BACK_TO_PRODUCTS = (By.CSS_SELECTOR, "[data-test=back-to-products]")

    def open(self):
        super().open(f"{BASE_URL}/inventory.html", wait_for=self.PRODUCT_LIST)
        return self

    # --- Каталог ---

    def product_names(self):
        return self.texts(self.PRODUCT_NAME)

    def product_prices(self):
        return self.texts(self.PRODUCT_PRICE)

    def product_images(self):
        self.texts(self.PRODUCT_NAME)
        return [img.get_attribute("src") for img in self.driver.find_elements(*self.PRODUCT_IMAGE)]

    def product_card(self, name):
        """Карточка товара в каталоге по точному названию (ждём отрисовку списка)."""
        try:
            return self.wait.until(
                lambda _: self.card_by_name(self.PRODUCT_LIST, self.PRODUCT_NAME, name)
            )
        except TimeoutException:
            raise AssertionError(f"Товар «{name}» не найден в каталоге")

    def product_price(self, name):
        return self.product_card(name).find_element(*self.PRODUCT_PRICE).text

    def sort_by(self, value):
        """value: az, za, lohi, hilo — значения из выпадающего списка сортировки."""
        Select(self.find(self.SORT_SELECT)).select_by_value(value)

    def wait_product_names(self, expected):
        self.wait.until(lambda _: self.product_names() == expected)

    def wait_product_prices(self, expected):
        self.wait.until(lambda _: self.product_prices() == expected)

    def add_to_cart(self, name):
        """Добавляет товар и ждёт, пока счётчик корзины вырастет; иначе повторяет клик."""
        expected = self.cart_count() + 1
        for attempt in range(3):
            if self.cart_count() == expected:  # клик уже сработал, а ожидание не успело
                return
            button = self.product_card(name).find_element(
                By.CSS_SELECTOR, "[data-test^='add-to-cart-']")
            button.click()
            try:
                self.wait.until(lambda _: self.cart_count() == expected)
                return
            except TimeoutException:
                if attempt == 2:
                    raise

    def open_product(self, name):
        """Открываем карточку товара кликом по его названию в каталоге."""
        name_link = self.product_card(name).find_element(*self.PRODUCT_NAME)
        self.click_until(name_link, EC.url_contains("inventory-item.html"))

    # --- Карточка товара ---

    def detail_name(self):
        return self.text(self.PRODUCT_NAME)

    def detail_price(self):
        return self.text(self.PRODUCT_PRICE)

    def back_to_products(self):
        self.click(self.BACK_TO_PRODUCTS)
