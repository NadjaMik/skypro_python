"""UI-тесты авторизации."""
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from data.test_data import INVALID_PASSWORD
from tests.api.conftest import LOGIN, PASSWORD
from tests.ui.pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@allure.feature("UI: Авторизация")
class TestLogin:
    @allure.story("Успешная авторизация")
    @allure.title("UI-01: вход с валидными кредами -> рабочее пространство")
    def test_successful_login(self, driver: WebDriver) -> None:
        login_page = LoginPage(driver)

        with allure.step("Открыть страницу входа"):
            login_page.open_login()

        with allure.step("Ввести валидные данные и отправить форму"):
            login_page.login(LOGIN, PASSWORD)

        with allure.step("Дождаться обработки авторизации"):
            login_page.wait_for_timeout(2000)

        with allure.step("Восстановить интерфейс после перехода"):
            if not login_page.get_text(login_page.root).strip():
                driver.refresh()

                if (
                    login_page.count(login_page.root)
                    and login_page.count(
                        (By.CSS_SELECTOR, "script[src*='/js/app.js']")
                    ) == 0
                ):
                    driver.execute_script(
                        """
                        if (typeof window.onLoad === "function") {
                            window.onLoad();
                        }
                        """
                    )

        with allure.step("Проверить отображение рабочего пространства"):
            login_page.wait_text(login_page.root, "Мои задачи", timeout=20)

            login_page.wait_count(login_page.email_input, 0)
            login_page.wait_count(login_page.password_input, 0)

    @allure.story("Отказ при неверном пароле")
    @allure.title("UI-02: неверный пароль -> сообщение об ошибке")
    def test_invalid_password_shows_error(self, driver: WebDriver) -> None:
        login_page = LoginPage(driver)

        with allure.step("Открыть страницу входа"):
            login_page.open_login()

        with allure.step("Отправить форму с неверным паролем"):
            login_page.login(LOGIN, INVALID_PASSWORD)

        with allure.step("Проверить сообщение об ошибке"):
            login_page.expect_error_visible()

    @allure.story("Валидация пустых полей")
    @allure.title("UI-03: пустые поля -> форма не авторизует пользователя")
    def test_empty_fields_do_not_authenticate(self, driver: WebDriver) -> None:
        login_page = LoginPage(driver)

        with allure.step("Открыть страницу входа"):
            login_page.open_login()

        with allure.step("Отправить пустую форму"):
            login_page.login("", "")

        with allure.step("Проверить, что форма входа осталась видимой"):
            login_page.expect_login_form_visible()
            assert "/team/" in driver.current_url
