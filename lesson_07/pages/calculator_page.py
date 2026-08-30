from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CalculatorPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(
            "https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html"
        )

    def set_delay(self, value: str):
        delay_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "delay"))
        )
        delay_input.clear()
        delay_input.send_keys(value)

    def click_button(self, text: str):
        btn = self.driver.find_element(
            By.XPATH, f"//span[text()='{text}']"
        )
        btn.click()

    def wait_for_result(self, expected_text: str, timeout: int):
        result_wait = WebDriverWait(self.driver, timeout)
        result_wait.until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "screen"), expected_text
            )
        )

    def get_result_text(self) -> str:
        screen = self.driver.find_element(By.CLASS_NAME, "screen")
        return screen.text