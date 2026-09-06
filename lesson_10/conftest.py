"""Глобальные фикстуры pytest для проекта lesson_10."""

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура создаёт экземпляр Chrome WebDriver.

    После завершения теста прикрепляет скриншот, если тест упал,
    и корректно закрывает браузер.
    """
    browser = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )
    browser.maximize_window()

    yield browser

    # Прикрепить скриншот при падении теста
    if hasattr(browser, "get_screenshot_as_png"):
        allure.attach(
            browser.get_screenshot_as_png(),
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG,
        )

    browser.quit()
