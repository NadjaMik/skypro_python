from selenium import webdriver
from pages.calculator_page import CalculatorPage


def test_slow_calculator():
    driver = webdriver.Chrome()

    try:
        calculator = CalculatorPage(driver)
        calculator.open()
        calculator.set_delay("45")

        for btn_text in ["7", "+", "8", "="]:
            calculator.click_button(btn_text)

        calculator.wait_for_result("15", 45)
        result = calculator.get_result_text()

        assert result == "15", (
            f"Ошибка: ожидался результат '15', но получено '{result}'"
        )

    finally:
        driver.quit()