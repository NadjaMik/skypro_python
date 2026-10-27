"""Тестовые данные и генераторы уникальных значений."""
import uuid


def unique_title(prefix: str) -> str:
    """Возвращает уникальное название сущности для изоляции тестов."""
    return f"{prefix} {uuid.uuid4().hex[:8]}"


PROJECT_TITLE = "Auto Project"
UPDATED_TITLE = "Auto Project (updated)"
BOARD_TITLE = "Auto Board"
COLUMN_TITLE = "New Column"
INVALID_PASSWORD = "wrong_password"
NON_EXISTENT_ID = "00000000-0000-0000-0000-000000000000"
