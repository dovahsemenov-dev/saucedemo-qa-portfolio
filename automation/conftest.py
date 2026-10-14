"""Фикстуры pytest: браузер, авторизация и скриншот при падении."""

import base64
import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pytest_html import extras

from config import PASSWORD, STANDARD_USER
from pages.login_page import LoginPage


@pytest.fixture
def driver():
    """Chrome 1920x1080; headless включается переменной окружения HEADLESS=1."""
    options = Options()
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    # Ждём только DOMContentLoaded — остальное отслеживаем явными ожиданиями в тестах.
    options.page_load_strategy = "eager"

    # Драйвер скачивается встроенным Selenium Manager, webdriver-manager не нужен.
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def logged_in(driver):
    """Авторизованный стандартным пользователем браузер (открыт каталог)."""
    LoginPage(driver).login_as_standard_user()
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """При падении теста прикрепляет скриншот к отчёту pytest-html."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    driver = item.funcargs.get("driver")
    if driver is None:
        return

    screenshot = base64.b64encode(driver.get_screenshot_as_png()).decode()
    report.extras = getattr(report, "extras", []) + [extras.png(screenshot)]
