from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def fill_first_name(self, first_name: str):
        self.wait.until(
            EC.presence_of_element_located((By.ID, "first-name"))
        ).send_keys(first_name)

    def fill_last_name(self, last_name: str):
        self.driver.find_element(By.ID, "last-name").send_keys(last_name)

    def fill_postal_code(self, postal_code: str):
        self.driver.find_element(By.ID, "postal-code").send_keys(postal_code)

    def click_continue(self):
        self.driver.find_element(By.ID, "continue").click()

    def get_total_text(self) -> str:
        total_label = self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "summary_total_label")
            )
        )
        return total_label.text