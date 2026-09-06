"""Автотесты для интернет-магазина SauceDemo с Allure-отчётностью."""

import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("Интернет-магазин SauceDemo")
@allure.severity(allure.severity_level.CRITICAL)
class TestSauceDemoCheckout:
    """Набор тестов для проверки полного цикла оформления заказа."""

    @allure.title("Успешное оформление заказа на 3 товара")
    @allure.description(
        "Авторизуемся, добавляем 3 товара в корзину, оформляем заказ и "
        "проверяем, что итоговая сумма равна $58.29."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_sauce_demo_checkout(self, driver) -> None:
        """
        E2E-тест оформления заказа в SauceDemo.

        :param driver: Фикстура WebDriver (из conftest.py).
        """
        # ── Шаг 1: Авторизация ──
        with allure.step("1. Авторизация пользователя"):
            login_page = LoginPage(driver)
            login_page.open()
            login_page.enter_username("standard_user")
            login_page.enter_password("secret_sauce")
            login_page.click_login()

        # ── Шаг 2: Каталог товаров ──
        with allure.step("2. Добавление товаров в корзину"):
            inventory_page = InventoryPage(driver)
            inventory_page.wait_for_load()

            products = [
                "add-to-cart-sauce-labs-backpack",
                "add-to-cart-sauce-labs-bolt-t-shirt",
                "add-to-cart-sauce-labs-onesie",
            ]
            for product_id in products:
                inventory_page.add_product_to_cart(product_id)

            inventory_page.go_to_cart()

        # ── Шаг 3: Корзина ──
        with allure.step("3. Переход к оформлению заказа"):
            cart_page = CartPage(driver)
            cart_page.click_checkout()

        # ── Шаг 4: Оформление заказа ──
        with allure.step("4. Заполнение данных покупателя"):
            checkout_page = CheckoutPage(driver)
            checkout_page.fill_first_name("Иван")
            checkout_page.fill_last_name("Петров")
            checkout_page.fill_postal_code("123456")
            checkout_page.click_continue()

        # ── Шаг 5: Проверка итоговой суммы ──
        with allure.step("5. Проверка итоговой суммы заказа"):
            total_text = checkout_page.get_total_text()
            assert "$58.29" in total_text, (
                f"Ошибка: ожидалась сумма $58.29, но получено '{total_text}'"
            )
