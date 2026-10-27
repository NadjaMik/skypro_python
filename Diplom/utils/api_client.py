"""HTTP-клиент для REST API YouGile v2."""
from typing import Any

import requests


class YougileApiClient:
    """Тонкая обёртка над requests.Session для API-тестов."""

    def __init__(self, base_url: str, timeout: float = 15.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def set_token(self, token: str) -> None:
        """Устанавливает Bearer-токен для последующих запросов."""
        self.session.headers["Authorization"] = f"Bearer {token}"

    def get_companies(self, login: str, password: str, company: str) -> dict[str, Any]:
        """Возвращает список доступных компаний."""
        response = self.session.post(
            f"{self.base_url}/auth/companies",
            json={"login": login, "password": password, "name": company},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def create_token(self, login: str, password: str, company_id: str) -> str:
        """Создаёт API-ключ и возвращает его значение."""
        response = self.session.post(
            f"{self.base_url}/auth/keys",
            json={"login": login, "password": password, "companyId": company_id},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return str(response.json()["key"])

    def create_project(self, title: str) -> dict[str, Any]:
        """Создаёт проект."""
        response = self.session.post(
            f"{self.base_url}/projects", json={"title": title, "users": {}},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get_project(self, project_id: str) -> dict[str, Any]:
        """Возвращает проект по ID."""
        response = self.session.get(
            f"{self.base_url}/projects/{project_id}", timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def update_project(self, project_id: str, title: str) -> dict[str, Any]:
        """Обновляет название проекта."""
        response = self.session.put(
            f"{self.base_url}/projects/{project_id}",
            json={"title": title}, timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def delete_project(self, project_id: str) -> requests.Response:
        """Удаляет проект, созданный тестом."""
        response = self.session.delete(
            f"{self.base_url}/projects/{project_id}", timeout=self.timeout
        )
        response.raise_for_status()
        return response

    def create_board(self, title: str, project_id: str) -> dict[str, Any]:
        """Создаёт доску в проекте."""
        payload = {
            "title": title,
            "projectId": project_id,
            "stickers": {
                "timer": False, "deadline": True, "stopwatch": True,
                "timeTracking": True, "assignee": True, "repeat": True,
            },
        }
        response = self.session.post(
            f"{self.base_url}/boards", json=payload, timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def create_column(self, title: str, color: int, board_id: str) -> dict[str, Any]:
        """Создаёт колонку на доске."""
        response = self.session.post(
            f"{self.base_url}/columns",
            json={"title": title, "color": color, "boardId": board_id},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def raw(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """Отправляет запрос без автоматической проверки статус-кода."""
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, f"{self.base_url}{path}", **kwargs)
