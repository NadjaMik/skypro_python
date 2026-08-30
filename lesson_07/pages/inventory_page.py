from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_load(self):
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

    def add_product_to_cart(self, product_id: str):
        self.driver.find_element(By.ID, product_id).click()

    def go_to_cart(self):
        self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()