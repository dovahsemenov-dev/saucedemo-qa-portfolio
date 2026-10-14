"""Тесты авторизации: позитив, негатив и выход из системы."""

import pytest

from config import LOCKED_OUT_USER, PASSWORD, STANDARD_USER
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_successful_login_standard_user(driver):
    page = LoginPage(driver).open().login(STANDARD_USER, PASSWORD)

    assert "inventory.html" in page.driver.current_url

def test_locked_out_user_sees_error(driver):
    page = LoginPage(driver).open().login(LOCKED_OUT_USER, PASSWORD)

    assert page.is_error_visible()
    assert "locked out" in page.error_text().lower()

@pytest.mark.parametrize("username, password, expected_error", [
    ("", "secret_sauce", "Username is required"),
    (STANDARD_USER, "", "Password is required"),
    (STANDARD_USER, "wrong_password", "do not match any user"),
    ("nonexistent_user", "secret_sauce", "do not match any user"),
])
def test_negative_login_shows_expected_error(driver, username, password, expected_error):
    page = LoginPage(driver).open().login(username, password)

    assert page.is_error_visible()
    assert expected_error in page.error_text()

def test_logout_through_menu(logged_in):
    page = LoginPage(logged_in)

    page.logout()

    assert page.is_error_visible() is False
    assert page.is_displayed(LoginPage.LOGIN_BUTTON)
