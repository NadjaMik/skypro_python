"""
Перед запуском тестов нужно внести переменные окружения:
  - YOUGILE_TOKEN — ваш Bearer-токен авторизации (обязательно)
  - YOUGILE_BASE_URL — базовый URL API (по умолчанию https://ru.yougile.com/api-v2)
"""

import os

YOUGILE_TOKEN = os.getenv("YOUGILE_TOKEN", "")
YOUGILE_BASE_URL = os.getenv("YOUGILE_BASE_URL", "https://ru.yougile.com/api-v2")