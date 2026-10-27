
"""Страница доски YouGile."""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from tests.ui.pages.base_page import BasePage, text_locator


class BoardPage(BasePage):
    """Page Object для работы с колонками доски."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

        self.add_column_button = (
            By.XPATH,
            "//button[normalize-space(.)='Создать колонку' or @aria-label='Создать колонку']"
            " | //*[@role='button'][normalize-space(.)='Создать колонку'"
            " or @aria-label='Создать колонку']",
        )

        self.column_title_input = (
            By.XPATH,
            "//input[@placeholder='Введите имя колонки…' or @aria-label='Введите имя колонки…']"
            " | //textarea[@placeholder='Введите имя колонки…'"
            " or @aria-label='Введите имя колонки…']",
        )

    def create_column(self, title: str) -> None:
        """Создаёт колонку и проверяет её отображение."""

        self.click(self.add_column_button)

        self.wait_visible(self.column_title_input, timeout=10)
        self.fill(self.column_title_input, title)
        self.press(self.column_title_input, Keys.ENTER)

        # Название колонки может отображаться вместе с числом задач.
        self.wait_any_visible(text_locator(title, exact=False), timeout=15)

    def expect_column_visible(self, title: str) -> None:
        """Проверяет отображение созданной колонки."""

        self.wait_any_visible(text_locator(title, exact=False), timeout=15)
