from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_sauce_demo_checkout():
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Открываем сайт
        driver.get("https://www.saucedemo.com/")

        # 2. Авторизуемся
        wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # 3. Ждём загрузки каталога
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

        # 4. Добавляем товары в корзину
        products = [
            "add-to-cart-sauce-labs-backpack",
            "add-to-cart-sauce-labs-bolt-t-shirt",
            "add-to-cart-sauce-labs-onesie",
        ]
        for product_id in products:
            driver.find_element(By.ID, product_id).click()

        # 5. Переходим в корзину
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # 6. Нажимаем Checkout
        wait.until(EC.presence_of_element_located((By.ID, "checkout"))).click()

        # 7. Заполняем форму
        wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Иван")
        driver.find_element(By.ID, "last-name").send_keys("Петров")
        driver.find_element(By.ID, "postal-code").send_keys("123456")

        # 8. Продолжаем
        driver.find_element(By.ID, "continue").click()

        # 9. Читаем итоговую сумму
        total_label = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )
        total_text = total_label.text  # например: "Total: $58.29"

        # 10. Проверяем сумму
        assert "$58.29" in total_text, (
            f"Ошибка: ожидалась сумма $58.29, но получено '{total_text}'"
        )

    finally:
        driver.quit()