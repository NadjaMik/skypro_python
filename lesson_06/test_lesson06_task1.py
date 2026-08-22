import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_dynamic_loading():
    driver = webdriver.Chrome()

    # 1. Откройте страницу
    driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")

    # 2. Найдите и нажмите на кнопку "Start" (CSS-селектор)
    start_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
    )
    start_button.click()

    # 3. Дождитесь появления текста "Hello World!" (явное ожидание)
    finish_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )
    hello_text = finish_element.text

    # 4. Создаём папку screenshots (если её нет) и сохраняем скриншот в неё
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshots_dir, "dynamic_loading_2.png")
    driver.save_screenshot(screenshot_path)

    # 5. Проверьте, что появившийся текст равен "Hello World!"
    assert hello_text == "Hello World!", (
         f"Expected 'Hello World!' but got '{hello_text}'")

    driver.quit()


test_dynamic_loading()
