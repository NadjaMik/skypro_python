"""Page Object для страницы корзины."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Класс страницы корзины покупок."""

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы корзины.

        :param driver: Экземпляр WebDriver.
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    @allure.step("Нажать кнопку Checkout")
    def click_checkout(self) -> None:
        """Нажимает кнопку перехода к оформлению заказа."""
        self.wait.until(
            EC.presence_of_element_located((By.ID, "checkout"))
        ).click()
