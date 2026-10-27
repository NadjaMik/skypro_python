
"""Страница авторизации YouGile."""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from config.settings import settings
from tests.ui.pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object страницы входа."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

        self.email_input = (By.CSS_SELECTOR, "input[type='email']")
        self.password_input = (By.CSS_SELECTOR, "input[type='password']")
        self.submit_button = (
            By.XPATH,
            "//button[normalize-space(.)='Войти' or @aria-label='Войти']"
            " | //*[@role='button'][normalize-space(.)='Войти' or @aria-label='Войти']",
        )
        self.error_message = (
            By.CSS_SELECTOR,
            ".alert-danger, .error, [class*='error'], [class*='invalid']",
        )
        self.root = (By.CSS_SELECTOR, "#root")

    def open_login(self) -> None:
        """Открывает страницу входа и инициализирует приложение."""
        self.open(f"{settings.ui_base_url}/team/")

        # Сначала проверяем обычную загрузку формы.
        try:
            self.wait_visible(self.email_input, timeout=3)
            self.wait_visible(self.password_input, timeout=3)
            return
        except TimeoutException:
            pass

        # Если форма не появилась, пробуем вызвать инициализацию приложения.
        on_load_type = self.driver.execute_script("return typeof window.onLoad")

        if on_load_type == "function":
            self.driver.execute_script("return window.onLoad()")

        # Проверяем, что форма действительно появилась.
        self.wait_visible(self.email_input, timeout=20)
        self.wait_visible(self.password_input, timeout=20)

    def login(self, email: str, password: str) -> None:
        """Заполняет форму и отправляет её."""
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.submit_button)

    def expect_error_visible(self) -> None:
        """Проверяет отображение ошибки авторизации."""
        self.wait_visible(self.error_message)

    def expect_login_form_visible(self) -> None:
        """Проверяет отображение формы авторизации."""
        self.wait_visible(self.email_input)
        self.wait_visible(self.password_input)
