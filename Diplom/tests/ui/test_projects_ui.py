
"""UI-тесты проектов, досок и выхода из системы."""

import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from data.test_data import unique_title
from tests.ui.pages.base_page import BasePage, by_test_id, text_locator, xpath_literal
from tests.ui.pages.board_page import BoardPage
from tests.ui.pages.projects_page import ProjectsPage

pytestmark = pytest.mark.ui


@allure.feature("UI: Проекты")
class TestProjects:
    @allure.story("Создание проекта")
    @allure.title("UI-04: созданный проект отображается")
    def test_create_project_visible(self, logged_in_driver: WebDriver) -> None:
        projects_page = ProjectsPage(logged_in_driver)
        title = unique_title("UI Project")
        project_created = False

        try:
            with allure.step("Создать проект с уникальным названием"):
                projects_page.create_project(title)
                project_created = True

            with allure.step("Проверить отображение проекта"):
                projects_page.expect_project_visible(title)

        finally:
            if project_created:
                with allure.step("Удалить созданный тестовый проект"):
                    projects_page.delete_project(title)


@allure.feature("UI: Сессия")
class TestSession:
    @allure.story("Завершение сессии")
    @allure.title("UI: пользователь может выйти из системы")
    def test_logout(self, logged_in_driver: WebDriver) -> None:
        base_page = BasePage(logged_in_driver)
        root = "//*[@id='root']"

        with allure.step("Открыть меню профиля"):
            base_page.click(by_test_id("profile-menu-item"))

        with allure.step("Выбрать выход из аккаунта"):
            logout_item = text_locator("Выход из аккаунта", exact=True)
            base_page.wait_visible(logout_item, timeout=10)
            base_page.click(logout_item)

        with allure.step("Проверить отображение формы авторизации"):
            base_page.wait_visible(
                (By.CSS_SELECTOR, "#root input[type='email']"), timeout=15
            )

            base_page.wait_visible(
                (By.CSS_SELECTOR, "#root input[type='password']"), timeout=10
            )

            base_page.wait_visible(
                text_locator("Войти:", exact=True, scope=root), timeout=10
            )


@allure.feature("UI: Доски")
class TestBoards:
    @allure.story("Создание колонки")
    @allure.title("UI-05: созданная колонка отображается на доске")
    def test_create_column_visible(self, logged_in_driver: WebDriver) -> None:
        projects_page = ProjectsPage(logged_in_driver)
        board_page = BoardPage(logged_in_driver)

        project_title = unique_title("UI Column Project")
        column_title = unique_title("UI Column")
        project_created = False

        try:
            with allure.step("Создать отдельный тестовый проект"):
                projects_page.create_project(project_title)
                project_created = True
                projects_page.expect_project_visible(project_title)

            with allure.step("Открыть тестовый проект"):
                project = (
                    By.XPATH,
                    "//*[@data-testid='project-item']"
                    f"[contains(., {xpath_literal(project_title)})]",
                )

                board_page.wait_visible(project, timeout=10)
                board_page.click(project)

            with allure.step("Проверить доступность создания колонки"):
                board_page.wait_visible(board_page.add_column_button, timeout=15)

            with allure.step("Создать колонку"):
                board_page.create_column(column_title)

            with allure.step("Проверить отображение колонки"):
                board_page.expect_column_visible(column_title)

        finally:
            if project_created:
                with allure.step("Удалить тестовый проект"):
                    projects_page.delete_project(project_title)
