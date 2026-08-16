from selenium import webdriver
from selenium.webdriver.common.by import By


def test_multiple_elements():
    driver = webdriver.Chrome()
    driver.get("https://httpbin.qa-territory.online/links/10")

    # Находим все ссылки на странице
    links = driver.find_elements(By.TAG_NAME, "a")

    # Проверяем количество ссылок
    assert len(links) == 9, f"Ожидалось 9 ссылок, найдено {len(links)}"

    # Проверяем, что все ссылки отображаются
    for link in links:
        assert link.is_displayed(), "Одна из ссылок не отображается"

    # Проверяем, что текст первой ссылки содержит "1"
    first_link_text = links[0].text
    assert "1" in first_link_text, f"Не содержит 1:'{first_link_text}'"

    driver.quit()


test_multiple_elements()
