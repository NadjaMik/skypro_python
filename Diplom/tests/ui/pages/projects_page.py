
"""Страница проектов YouGile."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from tests.ui.pages.base_page import BasePage, by_test_id, text_locator, xpath_literal


class ProjectsPage(BasePage):
    """Page Object страницы проектов."""

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

        self.add_project_button = by_test_id("add-project-button")
        self.default_project_menu_item = by_test_id("menu-item-add-default-project")
        self.project_name_input = (
            By.CSS_SELECTOR,
            'input[placeholder="Введите название проекта…"]',
        )
        self.confirm_create_button = (
            By.XPATH,
            "//button[normalize-space(.)='Добавить проект с задачами'"
            " or @aria-label='Добавить проект с задачами']"
            " | //*[@role='button'][normalize-space(.)='Добавить проект с задачами'"
            " or @aria-label='Добавить проект с задачами']",
        )
        self.project_cards = by_test_id("project-card")

    def create_project(self, title: str) -> None:
        """Создаёт обычный проект с задачами."""
        if self.get_attribute(self.add_project_button, "aria-expanded") != "true":
            self.click(self.add_project_button)

        self.click(self.default_project_menu_item)

        self.wait_visible(self.project_name_input, timeout=10)
        self.fill(self.project_name_input, title)

        self.wait_visible(self.confirm_create_button, timeout=10)
        self.click(self.confirm_create_button)

    def expect_project_visible(self, title: str) -> None:
        """Проверяет, что созданный проект отображается в интерфейсе."""
        self.wait_visible(text_locator(title, exact=False), timeout=15)

    def delete_project(self, title: str) -> None:
        """Удаляет созданный тестом проект и проверяет результат."""

        # Переходим к списку проектов компании.
        self.click(by_test_id("my-company-item"))

        project_card = (
            By.XPATH,
            f"//*[@data-testid='project-card'][contains(., {xpath_literal(title)})]",
        )

        # Убеждаемся, что найден ровно один нужный проект.
        self.wait_count(project_card, 1, timeout=15)

        # Открываем меню именно этого проекта.
        self.click(
            (
                By.XPATH,
                project_card[1] + "//*[@data-testid='project-card-menu-button']",
            )
        )

        # Выбираем удаление.
        self.click(by_test_id("menu-item-remove"))

        # Проверяем, что появилось подтверждение удаления.
        self.wait_visible(text_locator("Удалить проект?", exact=True), timeout=10)

        # Подтверждаем удаление.
        delete_button = text_locator("Удалить", exact=True)

        self.wait_visible(delete_button, timeout=10, index=-1)
        self.click(delete_button, index=-1)

        # Проверяем, что проект исчез из списка.
        self.wait_count(project_card, 0, timeout=15)
