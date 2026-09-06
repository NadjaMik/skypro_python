"""Page Object для страницы оформления заказа."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    """Класс страницы оформления заказа (Checkout)."""

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы оформления заказа.

        :param driver: Экземпляр WebDriver.
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    @allure.step("Заполнить поле First Name: {first_name}")
    def fill_first_name(self, first_name: str) -> None:
        """
        Вводит имя в поле First Name.

        :param first_name: Имя покупателя.
        """
        self.wait.until(
            EC.presence_of_element_located((By.ID, "first-name"))
        ).send_keys(first_name)

    @allure.step("Заполнить поле Last Name: {last_name}")
    def fill_last_name(self, last_name: str) -> None:
        """
        Вводит фамилию в поле Last Name.

        :param last_name: Фамилия покупателя.
        """
        self.driver.find_element(By.ID, "last-name").send_keys(last_name)

    @allure.step("Заполнить поле Zip/Postal Code: {postal_code}")
    def fill_postal_code(self, postal_code: str) -> None:
        """
        Вводит почтовый индекс в поле Zip/Postal Code.

        :param postal_code: Почтовый индекс.
        """
        self.driver.find_element(By.ID, "postal-code").send_keys(postal_code)

    @allure.step("Нажать кнопку Continue")
    def click_continue(self) -> None:
        """Нажимает кнопку продолжения оформления заказа."""
        self.driver.find_element(By.ID, "continue").click()

    @allure.step("Получить итоговую сумму заказа")
    def get_total_text(self) -> str:
        """
        Возвращает текст с итоговой суммой заказа.

        :return: Строка с итоговой суммой (например, 'Total: $58.29').
        """
        total_label = self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "summary_total_label")
            )
        )
        return total_label.text
