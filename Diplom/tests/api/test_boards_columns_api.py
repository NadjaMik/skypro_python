"""API-тесты досок и колонок (TC-06, TC-07)."""
from typing import Any, Dict

import allure
import pytest

from data.test_data import BOARD_TITLE, COLUMN_TITLE, unique_title
from utils.api_client import YougileApiClient

pytestmark = pytest.mark.api


@allure.feature("Доски и колонки")
class TestBoardsColumns:

    @allure.story("Создание доски в проекте")
    @allure.title("TC-06: создание доски в проекте -> 201")
    def test_create_board(
        self,
        api_client: YougileApiClient,
        auth_token: str,
        created_project: Dict[str, Any],
    ) -> None:
        board = api_client.create_board(
            unique_title(BOARD_TITLE), created_project["id"]
    )
        assert board.get("id"), f"В ответе нет id доски: {board}"



    @allure.story("Создание колонки на доске")
    @allure.title("TC-07: создание колонки на доске -> 201")
    def test_create_column(
        self,
        api_client: YougileApiClient,
        auth_token: str,
        created_project: Dict[str, Any],
    ) -> None:
        board = api_client.create_board(
            unique_title(BOARD_TITLE), created_project["id"]
    )
        column = api_client.create_column(COLUMN_TITLE, 3, board["id"])
        assert column.get("id"), f"В ответе нет id колонки: {column}"


