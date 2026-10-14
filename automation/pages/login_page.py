"""Страница авторизации https://www.saucedemo.com/."""

from selenium.webdriver.common.by import By

from config import BASE_URL, PASSWORD, STANDARD_USER
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    USERNAME = (By.CSS_SELECTOR, "[data-test=username]")
    PASSWORD = (By.CSS_SELECTOR, "[data-test=password]")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test=login-button]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test=error]")

    def open(self):
        super().open(BASE_URL, wait_for=self.USERNAME)
        return self

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def login_as_standard_user(self):
        """Быстрый вход валидным пользователем, возвращает страницу каталога."""
        self.open().login(STANDARD_USER, PASSWORD)
        self.wait.until(lambda _: "inventory" in self.driver.current_url)
        return InventoryPage(self.driver)

    def error_text(self):
        return self.text(self.ERROR_MESSAGE)

    def is_error_visible(self):
        return self.is_displayed(self.ERROR_MESSAGE)
