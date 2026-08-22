from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_slow_calculator():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Открываем страницу
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

        # 2. Вводим задержку 45
        delay_input = wait.until(EC.presence_of_element_located((By.ID, "delay")))
        delay_input.clear()
        delay_input.send_keys("45")

        # 3. Нажимаем кнопки: 7, +, 8, =
        for btn_text in ["7", "+", "8", "="]:
            btn = driver.find_element(By.XPATH, f"//span[text()='{btn_text}']")
            btn.click()

        # 4. Ждём результат 15 на экране
        result_wait = WebDriverWait(driver, 45)
        result_wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15")
        )

        # 5. Проверяем результат
        screen = driver.find_element(By.CLASS_NAME, "screen")
        assert screen.text == "15", (
            f"Ошибка: ожидался результат '15', но получено '{screen.text}'"
        )

    finally:
        driver.quit()