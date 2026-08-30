import pytest
import uuid
from config import YOUGILE_TOKEN, YOUGILE_BASE_URL
from pages.yougile_api import YougileAPI


@pytest.fixture(scope="session")
def api():
    """Один экземпляр PageObject на всю сессию"""
    assert YOUGILE_TOKEN, (
        "YOUGILE_TOKEN не задан"
        "Установите переменную окружения: export YOUGILE_TOKEN=\"your_token\""
    )
    return YougileAPI(YOUGILE_BASE_URL, YOUGILE_TOKEN)


@pytest.fixture
def unique_title():
    """Генерация уникального названия проекта"""
    return f"AutoTest_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def created_project(api, unique_title):
    """Создаёт проект перед тестом и удаляет. Возвращает ID созданного проекта"""
    response = api.create_project(title=unique_title)
    assert response.status_code == 201, (
        f"Не удалось создать проект: {response.status_code} — {response.text}"
    )
    project_id = response.json()["id"]

    yield project_id

    # Удаление проекта после теста
    api.delete_project(project_id)