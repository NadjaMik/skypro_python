"""API-тесты CRUD проектов (TC-03, TC-04, TC-05, TC-09, TC-10, TC-11)."""
from typing import Any, Dict

import allure
import pytest

from data.test_data import NON_EXISTENT_ID, UPDATED_TITLE, unique_title
from utils.api_client import YougileApiClient

pytestmark = pytest.mark.api


@allure.feature("Проекты")
class TestProjects:
    @allure.story("Создание проекта")
    @allure.title("TC-03: создание проекта -> 201, возвращается id")
    def test_create_project(
        self, api_client: YougileApiClient, auth_token: str
    ) -> None:
        title = unique_title("TC-03")

        project: Dict[str, Any] = {}

        try:
            with allure.step("Создать проект с уникальным названием"):
                project = api_client.create_project(title)

            with allure.step("Проверить, что API вернул id"):
                assert project.get("id"), "В ответе API отсутствует id проекта"

            with allure.step("Получить созданный проект и проверить название"):
                fetched_project = api_client.get_project(project["id"])
                assert fetched_project["id"] == project["id"]
                assert fetched_project["title"] == title
        finally:
            # Удаляем созданную тестом сущность даже при падении проверки.
            project_id = project.get("id")
            if project_id:
                with allure.step(f"Cleanup: удалить проект {project_id}"):
                    response = api_client.raw("DELETE", f"/projects/{project_id}")
                    if response.status_code not in (200, 202, 204, 404):
                        response.raise_for_status()



    @allure.story("Обновление проекта")
    @allure.title("TC-05: обновление названия проекта -> 200")
    def test_update_project(
        self,
        api_client: YougileApiClient,
        auth_token: str,
        created_project: Dict[str, Any],
    ) -> None:
        updated_title = unique_title(UPDATED_TITLE)

        with allure.step("Обновить название проекта"):
            response = api_client.update_project(
                created_project["id"], updated_title
            )

        with allure.step("Проверить успешный ответ API"):
            assert response.get("id") == created_project["id"], (
                f"Ожидался id {created_project['id']}, "
                f"получен ответ: {response}"
            )

        with allure.step("Получить проект и проверить новое название"):
            updated_project = api_client.get_project(
                created_project["id"]
            )
            assert updated_project["title"] == updated_title, (
                f"Ожидалось название {updated_title!r}, "
                f"получено {updated_project.get('title')!r}"
            )


    @allure.story("Валидация обязательного поля")
    @allure.title("TC-09: пустое название -> 400")
    def test_create_project_empty_title(
        self, api_client: YougileApiClient, auth_token: str
    ) -> None:
        payload = {"title": "", "users": {}}
        response = api_client.raw("POST", "/projects", json=payload)
        assert response.status_code == 400

    @allure.story("Обработка неизвестного проекта")
    @allure.title("TC-10: несуществующий ID -> 404")
    def test_get_project_not_found(
        self, api_client: YougileApiClient, auth_token: str
    ) -> None:
        response = api_client.raw("GET", f"/projects/{NON_EXISTENT_ID}")
        assert response.status_code == 404

    
    @allure.story("Неподдерживаемый HTTP-метод")
    @allure.title("TC-11: PATCH для проекта -> 404 Not Found")
    def test_patch_method_not_allowed(
        self,
        api_client: YougileApiClient,
        auth_token: str,
        created_project: Dict[str, Any],
    ) -> None:
        response = api_client.raw(
            "PATCH",
            f"/projects/{created_project['id']}",
            json={"title": "x"},
        )

        assert response.status_code == 404, (
            f"Ожидался 404 для неподдерживаемого PATCH, "
            f"получен {response.status_code}: {response.text}"
        )

        body = response.json()
        assert "Cannot PATCH" in body.get("message", ""), (
            f"Неожиданное сообщение API: {body}"
        )

