"""Page Object для страницы каталога товаров."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    """Класс страницы каталога товаров (Inventory)."""

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы каталога.

        :param driver: Экземпляр WebDriver.
        """
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    @allure.step("Дождаться загрузки списка товаров")
    def wait_for_load(self) -> None:
        """Ожидает появления списка товаров на странице."""
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

    @allure.step("Добавить товар в корзину: {product_id}")
    def add_product_to_cart(self, product_id: str) -> None:
        """
        Добавляет товар в корзину по его ID кнопки.

        :param product_id: HTML-идентификатор кнопки добавления товара.
        """
        self.driver.find_element(By.ID, product_id).click()

    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> None:
        """Нажимает на иконку корзины для перехода в корзину."""
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
