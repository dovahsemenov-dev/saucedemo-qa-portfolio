"""Общая база Page Object: явные ожидания, базовые действия и шапка сайта."""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import TIMEOUT


class BasePage:
    # Шапка повторяется на всех страницах после входа в магазин.
    CART_LINK = (By.CSS_SELECTOR, "[data-test=shopping-cart-link]")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test=shopping-cart-badge]")
    # Кнопка бургер-меню лежит поверх иконки data-test="open-menu",
    # поэтому кликаем именно по кнопке, иначе клик перехватывает иконка.
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.CSS_SELECTOR, "[data-test=logout-sidebar-link]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def open(self, url, wait_for=None):
        """Открывает страницу; при медленном стенде повторяет загрузку (до 3 раз)."""
        for attempt in range(3):
            try:
                self.driver.get(url)
            except TimeoutException:
                pass  # страница не успела загрузиться — проверяем ниже по локатору
            if wait_for is None:
                return self
            try:
                self.find(wait_for)
                return self
            except TimeoutException:
                if attempt == 2:
                    raise
        return self

    def find(self, locator):
        """Ждём, пока элемент появится на странице, и возвращаем его."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        """Ждём, пока элемент станет кликабельным, и кликаем."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text(self, locator):
        return self.find(locator).text

    def texts(self, locator):
        """Тексты всех элементов по локатору (список названий, цен и т.п.)."""
        self.wait.until(EC.presence_of_element_located(locator))
        return [element.text for element in self.driver.find_elements(*locator)]

    def is_displayed(self, locator):
        elements = self.driver.find_elements(*locator)
        return bool(elements) and elements[0].is_displayed()

    # --- Шапка ---

    def cart_count(self):
        """Число товаров в корзине: значение бейджа, 0 если бейджа нет."""
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def wait_cart_count(self, count):
        self.wait.until(lambda _: self.cart_count() == count)

    def open_cart(self):
        self.click(self.CART_LINK)

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        # После выхода мы возвращаемся на страницу логина без адреса inventory.
        self.wait.until(lambda _: "inventory" not in self.driver.current_url)
