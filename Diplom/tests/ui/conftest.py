
"""Фикстуры UI-тестов: браузер, страница, авторизованная страница."""

from collections.abc import Iterator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from tests.api.conftest import LOGIN, PASSWORD
from tests.ui.pages.login_page import LoginPage


@pytest.fixture()
def driver() -> Iterator[WebDriver]:
    """Новый изолированный браузер (Chrome) для каждого теста."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,720")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Аналог wait_until="domcontentloaded": не ждём полной загрузки ресурсов.
    options.page_load_strategy = "eager"

    driver = webdriver.Chrome(options=options)

    try:
        yield driver
    finally:
        driver.quit()


@pytest.fixture()
def logged_in_driver(driver: WebDriver) -> Iterator[WebDriver]:
    """Авторизованная страница с проверкой загрузки рабочего пространства."""
    login_page = LoginPage(driver)

    # Открываем страницу входа и авторизуемся.
    login_page.open_login()
    login_page.login(LOGIN, PASSWORD)

    # Даём приложению обработать авторизацию.
    login_page.wait_for_timeout(2000)

    # Если рабочее пространство не отобразилось,
    # перезагружаем страницу и повторяем инициализацию приложения.
    if not login_page.get_text(login_page.root).strip():
        driver.refresh()

        if login_page.count((By.CSS_SELECTOR, "script[src*='/js/app.js']")) == 0:
            driver.execute_script(
                """
                if (typeof window.onLoad === "function") {
                    window.onLoad();
                } else {
                    throw new Error(
                        "Не найдена функция инициализации приложения"
                    );
                }
                """
            )

    # Проверяем, что рабочее пространство загрузилось.
    login_page.wait_text(login_page.root, "Мои задачи", timeout=20)

    yield driver
