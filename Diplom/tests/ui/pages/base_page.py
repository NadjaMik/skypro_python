"""Базовый класс страниц (Page Object)."""
from typing import Callable

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings

Locator = tuple[str, str]


def by_test_id(test_id: str) -> Locator:
    """Локатор по атрибуту data-testid (аналог get_by_test_id)."""
    return By.CSS_SELECTOR, f"[data-testid='{test_id}']"


def xpath_literal(value: str) -> str:
    """Безопасно экранирует строку для XPath."""
    if "'" not in value:
        return f"'{value}'"
    if '"' not in value:
        return f'"{value}"'
    parts = value.split("'")
    return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"


def text_locator(text: str, exact: bool = False, scope: str = "") -> Locator:
    """Локатор по тексту элемента (аналог get_by_text).

    scope — необязательный XPath-префикс, ограничивающий область поиска.
    """
    literal = xpath_literal(text)
    if exact:
        condition = f"normalize-space(.)={literal}"
    else:
        condition = f"contains(., {literal})"
    return By.XPATH, f"{scope}//*[text()[{condition}]]"


class BasePage:
    """Общие действия для всех страниц."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.timeout: float = settings.default_timeout / 1000
        self.driver.set_page_load_timeout(self.timeout)

    def open(self, url: str) -> None:
        self.driver.get(url)

    # ---- ожидания ----------------------------------------------------

    def _wait(self, timeout: float | None) -> WebDriverWait:
        return WebDriverWait(self.driver, timeout or self.timeout, poll_frequency=0.2)

    def _element(self, locator: Locator, index: int = 0) -> WebElement | None:
        elements = self.driver.find_elements(*locator)
        try:
            return elements[index]
        except IndexError:
            return None

    def wait_visible(
        self, locator: Locator, timeout: float | None = None, index: int = 0
    ) -> WebElement:
        """Ждёт, пока элемент станет видимым."""

        def condition(_: WebDriver) -> WebElement | bool:
            element = self._element(locator, index)
            try:
                return element if element is not None and element.is_displayed() else False
            except StaleElementReferenceException:
                return False

        return self._wait(timeout).until(
            condition, message=f"Элемент не стал видимым: {locator}"
        )

    def wait_any_visible(self, locator: Locator, timeout: float | None = None) -> None:
        """Ждёт, пока хотя бы один из найденных элементов станет видимым."""

        def condition(_: WebDriver) -> bool:
            try:
                return any(e.is_displayed() for e in self.driver.find_elements(*locator))
            except StaleElementReferenceException:
                return False

        self._wait(timeout).until(
            condition, message=f"Нет видимых элементов: {locator}"
        )

    def wait_count(
        self, locator: Locator, count: int, timeout: float | None = None
    ) -> None:
        """Ждёт, пока количество найденных элементов станет равным count."""
        self._wait(timeout).until(
            lambda d: len(d.find_elements(*locator)) == count,
            message=f"Количество элементов {locator} не стало равным {count}",
        )

    def wait_text(
        self, locator: Locator, text: str, timeout: float | None = None
    ) -> None:
        """Ждёт, пока элемент будет содержать текст."""

        def condition(_: WebDriver) -> bool:
            element = self._element(locator)
            try:
                return element is not None and text in (
                    element.get_attribute("textContent") or ""
                )
            except StaleElementReferenceException:
                return False

        self._wait(timeout).until(
            condition, message=f"Элемент {locator} не содержит текст '{text}'"
        )

    # ---- действия ----------------------------------------------------

    def _retry_action(
        self,
        locator: Locator,
        action: Callable[[WebElement], None],
        timeout: float | None,
        index: int,
    ) -> None:
        """Повторяет действие, пока элемент не станет доступен для него."""

        def condition(_: WebDriver) -> bool:
            element = self._element(locator, index)
            if element is None:
                return False
            try:
                if not (element.is_displayed() and element.is_enabled()):
                    return False
                action(element)
                return True
            except (
                StaleElementReferenceException,
                ElementClickInterceptedException,
                ElementNotInteractableException,
            ):
                return False

        self._wait(timeout).until(
            condition, message=f"Не удалось выполнить действие над {locator}"
        )

    def click(
        self, locator: Locator, timeout: float | None = None, index: int = 0
    ) -> None:
        def action(element: WebElement) -> None:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                element,
            )
            element.click()

        self._retry_action(locator, action, timeout, index)

    def fill(self, locator: Locator, text: str, timeout: float | None = None) -> None:
        def action(element: WebElement) -> None:
            element.clear()
            if text:
                element.send_keys(text)

        self._retry_action(locator, action, timeout, 0)

    def press(self, locator: Locator, key: str, timeout: float | None = None) -> None:
        self._retry_action(locator, lambda e: e.send_keys(key), timeout, 0)

    # ---- чтение состояния -------------------------------------------

    def get_attribute(
        self, locator: Locator, name: str, timeout: float | None = None
    ) -> str | None:
        """Возвращает атрибут элемента, дождавшись его появления в DOM."""
        element = self._wait(timeout).until(
            lambda d: self._element(locator), message=f"Элемент не найден: {locator}"
        )
        return element.get_attribute(name)

    def get_text(self, locator: Locator) -> str:
        """Возвращает видимый текст элемента."""
        return self.driver.find_element(*locator).text

    def count(self, locator: Locator) -> int:
        return len(self.driver.find_elements(*locator))

