"""API-тесты авторизации (TC-01, TC-02, TC-08)."""
import allure
import pytest

from config.settings import settings
from data.test_data import INVALID_PASSWORD
from tests.api.conftest import LOGIN, PASSWORD
from utils.api_client import YougileApiClient

pytestmark = pytest.mark.api


@allure.feature("Авторизация")
@allure.story("Получение списка компаний")
class TestGetCompanies:
    @allure.story("Успешный запрос списка компаний")
    @allure.title("TC-01: список компаний возвращается со статусом 200")
    def test_get_companies_success(self, api_client: YougileApiClient) -> None:
        data = api_client.get_companies(LOGIN, PASSWORD, settings.company_name)
        assert "content" in data
        assert isinstance(data["content"], list) and len(data["content"]) > 0
        assert data["content"][0]["id"]


@allure.feature("Авторизация")
@allure.story("Создание API-ключа")
class TestCreateToken:
    @allure.story("Успешное создание API-ключа")
    @allure.title("TC-02: API-ключ успешно создаётся")
    def test_create_token_success(
        self, api_client: YougileApiClient, auth_token: str
    ) -> None:
        assert isinstance(auth_token, str)
        assert len(auth_token) > 0

    @allure.title("TC-08: неверный пароль -> 401, ключ не выдаётся")
    @allure.story("Отказ при неверном пароле")
    def test_create_token_wrong_password(
        self, api_client: YougileApiClient
    ) -> None:
        """Негативный сценарий не зависит от успешной авторизации."""
        if not LOGIN or not PASSWORD:
            pytest.fail("Для API-тестов задайте YOUGILE_LOGIN и YOUGILE_PASSWORD в .env")
        with allure.step("Получить идентификатор компании валидной учётной записью"):
            companies = api_client.get_companies(LOGIN, PASSWORD, settings.company_name)
        company_items = companies.get("content", [])
        assert company_items, f"Компания '{settings.company_name}' не найдена"
        company_id = str(company_items[0]["id"])
        payload = {"login": LOGIN, "password": INVALID_PASSWORD, "companyId": company_id}
        with allure.step("Попытаться создать ключ с неверным паролем"):
            response = api_client.raw("POST", "/auth/keys", json=payload)
        with allure.step("Проверить отказ в авторизации"):
            assert response.status_code == 401
            assert "key" not in response.json()
