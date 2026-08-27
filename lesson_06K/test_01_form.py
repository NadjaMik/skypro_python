from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form_validation():
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 10)

    try:
        # 1. Открываем страницу
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")

        # 2. Заполняем форму
        form_data = {
            "first-name": "Иван",
            "last-name": "Петров",
            "address": "Ленина, 55-3",
            "e-mail": "test@skypro.com",
            "phone": "+7985899998787",
            "city": "Москва",
            "country": "Россия",
            "job-position": "QA",
            "company": "SkyPro",
        }

        for field_id, value in form_data.items():
            field = wait.until(EC.presence_of_element_located((By.ID, field_id)))
            field.send_keys(value)


        # 3. Нажимаем Submit
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()

        # 4. Ждём появления валидации
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .alert-success"))
        )

        # 5. Проверяем Zip code — красный
        zip_field = driver.find_element(By.ID, "zip-code")
        zip_parent = zip_field.find_element(By.XPATH, "..")
        assert "alert-danger" in zip_parent.get_attribute("class"), (
            "Ошибка: поле Zip code должно быть подсвечено красным (alert-danger)"
        )

        # 6. Проверяем остальные поля — зелёные
        success_fields = [
            "first-name", "last-name", "address", "e-mail", "phone",
            "city", "country", "job-position", "company"
        ]

        for field_id in success_fields:
            field = driver.find_element(By.ID, field_id)
            parent = field.find_element(By.XPATH, "..")
            assert "alert-success" in parent.get_attribute("class"), (
                f"Ошибка: поле {field_id} должно быть подсвечено зелёным (alert-success)"
            )

    finally:
        driver.quit()