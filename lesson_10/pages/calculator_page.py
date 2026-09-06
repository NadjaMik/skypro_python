"""Page Object для страницы медленного калькулятора."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    """Класс страницы калькулятора с задержкой вычислений."""

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы калькулятора.

        :param driver: Экземпляр WebDriver.
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    @allure.step("Открыть страницу калькулятора")
    def open(self) -> None:
        """Открывает страницу медленного калькулятора."""
        self.driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
        )

    @allure.step("Установить задержку вычислений: {value} сек")
    def set_delay(self, value: str) -> None:
        """
        Устанавливает значение задержки перед вычислением.

        :param value: Значение задержки в секундах (строка).
        """
        delay_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "delay"))
        )
        delay_input.clear()
        delay_input.send_keys(value)

    @allure.step("Нажать кнопку калькулятора: {text}")
    def click_button(self, text: str) -> None:
        """
        Нажимает кнопку калькулятора по её тексту.

        :param text: Текст на кнопке (например, '7', '+', '=').
        """
        btn = self.driver.find_element(
            By.XPATH, f"//span[text()='{text}']"
        )
        btn.click()

    @allure.step("Ожидать результат {expected_text} с таймаутом {timeout} сек")
    def wait_for_result(self, expected_text: str, timeout: int) -> None:
        """
        Явное ожидание появления ожидаемого результата на экране.

        :param expected_text: Ожидаемый текст результата.
        :param timeout: Максимальное время ожидания в секундах.
        """
        result_wait = WebDriverWait(self.driver, timeout)
        result_wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "screen"), expected_text
            )
        )

    @allure.step("Получить текст результата с экрана калькулятора")
    def get_result_text(self) -> str:
        """
        Возвращает текущий текст с экрана калькулятора.

        :return: Текст результата вычисления.
        """
        screen = self.driver.find_element(By.CLASS_NAME, "screen")
        return screen.text
