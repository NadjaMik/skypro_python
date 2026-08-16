from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_form_submission():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.qa-territory.online/forms/post")
    sleep(2)

    # Ввод имени
    driver.find_element(By.NAME, "custname").send_keys("Nadja")
    sleep(2)

    # Сохраняем текущий URL до клика
    old_url = driver.current_url

    # Находим кнопку по тексту
    click_button = driver.find_element(By.XPATH,
                                       "//button[text()='Submit order']")
    click_button.click()
    sleep(5)

    # Проверяем, что URL изменился
    new_url = driver.current_url
    assert new_url != old_url, "URL не изменился после отправки формы"

    driver.quit()


test_form_submission()
