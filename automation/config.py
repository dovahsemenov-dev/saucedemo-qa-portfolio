"""Константы проекта: адрес стенда, учётные данные и тестовые пользователи."""

import os

BASE_URL = "https://www.saucedemo.com"

# Таймаут явных ожиданий; можно увеличить переменной окружения UI_TIMEOUT (в CI задано 30).
TIMEOUT = int(os.getenv("UI_TIMEOUT", "15"))

PASSWORD = "secret_sauce"

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
ERROR_USER = "error_user"
