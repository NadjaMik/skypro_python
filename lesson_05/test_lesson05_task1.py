from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


def test_navigation():
    driver = webdriver.Chrome()
    base_url = "https://httpbin.qa-territory.online"
    driver.get(base_url)
    sleep(2)

    click_button = driver.find_element(By.LINK_TEXT, 'HTML Form')
    click_button.click()
    sleep(2)

    expected_url = base_url + "/forms/post"
    assert driver.current_url == expected_url

    driver.back()
    sleep(2)

    # Проверяем, что вернулись на исходную страницу
    assert driver.current_url.rstrip('/') == base_url.rstrip('/')

    driver.quit()


test_navigation()
