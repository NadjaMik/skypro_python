import requests
from typing import Optional, Dict, Any


class YougileAPI:

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.projects_endpoint = f"{self.base_url}/projects"

    # POST /api-v2/projects  — Создание проекта
    def create_project(
        self,
        title: str,
        users: Optional[Dict[str, str]] = None,
        departments: Optional[Dict] = None,
        idempotency_key: Optional[str] = None
    ) -> requests.Response:
        """Создание нового проекта. Поле title — обязательное"""
        payload: Dict[str, Any] = {"title": title}
        if users is not None:
            payload["users"] = users
        if departments is not None:
            payload["departments"] = departments
        if idempotency_key is not None:
            payload["idempotencyKey"] = idempotency_key

        return requests.post(
            self.projects_endpoint,
            headers=self.headers,
            json=payload
        )

    # PUT /api-v2/projects/{id}  — Обновление проекта
    def update_project(
        self,
        project_id: str,
        title: Optional[str] = None,
        deleted: Optional[bool] = None,
        users: Optional[Dict[str, str]] = None,
        departments: Optional[Dict] = None
    ) -> requests.Response:
        """Обновление существующего проекта"""
        payload: Dict[str, Any] = {}
        if title is not None:
            payload["title"] = title
        if deleted is not None:
            payload["deleted"] = deleted
        if users is not None:
            payload["users"] = users
        if departments is not None:
            payload["departments"] = departments

        url = f"{self.projects_endpoint}/{project_id}"
        return requests.put(url, headers=self.headers, json=payload)

    # GET /api-v2/projects/{id}  — Получение проекта
    def get_project(self, project_id: str) -> requests.Response:
        """Возвращает проект по ID"""
        url = f"{self.projects_endpoint}/{project_id}"
        return requests.get(url, headers=self.headers)

    # Удаление проекта (через PUT)
    def delete_project(self, project_id: str) -> requests.Response:
        """Удаление проекта"""
        return self.update_project(project_id, deleted=True)