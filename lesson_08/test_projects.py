"""
Автотесты API Yougile: Projects (POST, PUT, GET)

Структура:
  - TestCreateProject  — тесты на создание проекта
  - TestUpdateProject  — тесты на обновление проекта
  - TestGetProject     — тесты на получение проекта

Каждый класс содержит позитивные и негативные сценарии
"""

import requests
import uuid


# POST /api-v2/projects
class TestCreateProject:
    """Тесты метода POST /api-v2/projects — создание проекта"""

    # Позитивные

    def test_create_project_with_valid_data(self, api, unique_title):
        """Создание проекта с валидным обязательным полем title"""
        response = api.create_project(title=unique_title)

        assert response.status_code == 201, (
            f"Ожидали 201, получили {response.status_code}: {response.text}"
        )
        data = response.json()
        assert "id" in data, "В ответе отсутствует поле id"
        assert isinstance(data["id"], str) and len(data["id"]) > 0

        # Удаляем созданный проект
        api.delete_project(data["id"])

    def test_create_project_with_idempotency_key(self, api, unique_title):
        """Повторный запрос с тем же id"""
        key = f"idem_{uuid.uuid4().hex}"

        r1 = api.create_project(title=unique_title, idempotency_key=key)
        assert r1.status_code == 201
        project_id_1 = r1.json()["id"]

        r2 = api.create_project(title=f"{unique_title}_2", idempotency_key=key)
        assert r2.status_code == 201
        project_id_2 = r2.json()["id"]

        # Один и тот же проект
        assert project_id_1 == project_id_2, (
            "IdempotencyKey не сработал: созданы разные проекты"
        )

        api.delete_project(project_id_1)

    # Негативные

    def test_create_project_without_title(self, api):
        """Запрос без обязательного поля title"""
        # Отправка пустого JSON, минуя валидацию PageObject
        response = requests.post(
            api.projects_endpoint,
            headers=api.headers,
            json={}
        )
        assert response.status_code in (400, 422), (
            f"Ожидали 400/422, получили {response.status_code}: {response.text}"
        )

    def test_create_project_with_empty_title(self, api):
        """Пустая строка в обязательном поле title"""
        response = api.create_project(title="")
        assert response.status_code in (400, 422), (
            f"Ожидали 400/422, получили {response.status_code}: {response.text}"
        )


# PUT /api-v2/projects/{id}
class TestUpdateProject:
    """Тесты метода PUT /api-v2/projects/{id} — обновление проекта"""

    # Позитивные

    def test_update_project_title(self, api, created_project, unique_title):
        """Обновление названия существующего проекта. Проверяем через GET, что изменения сохранились"""
        new_title = f"Updated_{unique_title}"
        response = api.update_project(created_project, title=new_title)

        assert response.status_code == 200, (
            f"Ожидали 200, получили {response.status_code}: {response.text}"
        )
        data = response.json()
        assert data["id"] == created_project

        # Проверяем, что изменения применились
        get_resp = api.get_project(created_project)
        assert get_resp.json()["title"] == new_title

    def test_update_project_soft_delete(self, api, created_project):
        """Удаление проекта через флаг deleted = true"""
        response = api.update_project(created_project, deleted=True)
        assert response.status_code == 200

        get_resp = api.get_project(created_project)
        assert get_resp.json()["deleted"] is True

    # Негативные

    def test_update_nonexistent_project(self, api):
        """Обновление проекта с несуществующим ID"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = api.update_project(fake_id, title="NewTitle")
        assert response.status_code == 404, (
            f"Ожидали 404, получили {response.status_code}: {response.text}"
        )

    def test_update_project_invalid_id_format(self, api):
        """Обновление с невалидным форматом ID"""
        response = api.update_project("not-a-uuid", title="Title")
        assert response.status_code == 400, (
            f"Ожидали 400, получили {response.status_code}: {response.text}"
        )


# GET /api-v2/projects/{id}
class TestGetProject:
    """Тесты метода GET /api-v2/projects/{id} — получение проекта"""

    # Позитивные

    def test_get_existing_project(self, api, created_project, unique_title):
        """Получение существующего проекта по ID"""
        response = api.get_project(created_project)

        assert response.status_code == 200, (
            f"Ожидали 200, получили {response.status_code}: {response.text}"
        )
        data = response.json()
        assert data["id"] == created_project
        assert "title" in data
        assert "timestamp" in data
        assert "deleted" in data
        assert isinstance(data["deleted"], bool)

    # Негативные

    def test_get_nonexistent_project(self, api):
        """Запрос несуществующего проекта"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = api.get_project(fake_id)
        assert response.status_code == 404, (
            f"Ожидали 404, получили {response.status_code}: {response.text}"
        )

    def test_get_project_invalid_id_format(self, api):
        """Запрос с невалидным форматом ID"""
        response = api.get_project("invalid-id-123")
        assert response.status_code == 400, (
            f"Ожидали 400, получили {response.status_code}: {response.text}"
        )