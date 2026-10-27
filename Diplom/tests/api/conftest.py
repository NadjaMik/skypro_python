"""Фикстуры API: клиент, авторизация и временные сущности."""
import os
from collections.abc import Iterator
from typing import Any

import allure
import pytest
from dotenv import load_dotenv

from config.settings import settings
from utils.api_client import YougileApiClient

load_dotenv()
LOGIN = os.getenv("YOUGILE_LOGIN", "").strip()
PASSWORD = os.getenv("YOUGILE_PASSWORD", "").strip()


@pytest.fixture(scope="session")
def api_client() -> YougileApiClient:
    """HTTP-клиент на весь тестовый прогон."""
    return YougileApiClient(settings.api_base_url, timeout=settings.default_timeout / 1000)


@pytest.fixture(scope="session")
def auth_token(api_client: YougileApiClient) -> str:
    """Получает API-ключ для тестовой компании."""
    if not LOGIN or not PASSWORD:
        pytest.fail(
            "Не заданы YOUGILE_LOGIN/YOUGILE_PASSWORD. "
            "Скопируйте .env.example в .env и укажите тестовую учётную запись."
        )
    with allure.step("Получить список компаний пользователя"):
        companies = api_client.get_companies(LOGIN, PASSWORD, settings.company_name)
    company_items = companies.get("content", [])
    if not company_items:
        pytest.fail(
            f"Для учётной записи не найдена компания '{settings.company_name}'. "
            "Проверьте config/config.ini."
        )
    company_id = str(company_items[0]["id"])
    with allure.step("Создать API-ключ для выбранной компании"):
        token = api_client.create_token(LOGIN, PASSWORD, company_id)
    api_client.set_token(token)
    return token


@pytest.fixture()
def created_project(
    api_client: YougileApiClient, auth_token: str
) -> Iterator[dict[str, Any]]:
    """Создаёт уникальный проект и пытается удалить его после теста."""
    import uuid

    project = api_client.create_project(f"Fixture Project {uuid.uuid4().hex[:8]}")
    try:
        yield project
    finally:
        with allure.step(f"Cleanup: удалить проект {project['id']}"):
            response = api_client.raw("DELETE", f"/projects/{project['id']}")
            if response.status_code not in (200, 202, 204, 404):
                response.raise_for_status()
