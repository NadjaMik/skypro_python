from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_sauce_demo_checkout():
    driver = webdriver.Firefox()

    try:
        login_page = LoginPage(driver)
        login_page.open()
        login_page.enter_username("standard_user")
        login_page.enter_password("secret_sauce")
        login_page.click_login()

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

        cart_page = CartPage(driver)
        cart_page.click_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_first_name("Иван")
        checkout_page.fill_last_name("Петров")
        checkout_page.fill_postal_code("123456")
        checkout_page.click_continue()

        total_text = checkout_page.get_total_text()

        assert "$58.29" in total_text, (
            f"Ошибка: ожидалась сумма $58.29, но получено '{total_text}'"
        )

    finally:
        driver.quit()