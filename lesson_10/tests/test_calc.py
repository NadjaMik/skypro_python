"""Автотесты для страницы медленного калькулятора с Allure-отчётностью."""

import allure
from pages.calculator_page import CalculatorPage


@allure.feature("Калькулятор")
@allure.severity(allure.severity_level.CRITICAL)
class TestCalculator:
    """Набор тестов для проверки работы медленного калькулятора."""

    @allure.title("Сложение 7 + 8 с задержкой 45 секунд")
    @allure.description(
        "Проверяем, что калькулятор корректно вычисляет сумму 7 + 8 = 15 "
        "при установленной задержке в 45 секунд."
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_slow_calculator(self, driver) -> None:
        """
        Тест сложения двух чисел с задержкой.

        :param driver: Фикстура WebDriver (из conftest.py).
        """
        calculator = CalculatorPage(driver)

        with allure.step("1. Открыть страницу калькулятора"):
            calculator.open()

        with allure.step("2. Установить задержку 45 секунд"):
            calculator.set_delay("45")

        with allure.step("3. Нажать последовательность: 7, +, 8, ="):
            for btn_text in ["7", "+", "8", "="]:
                calculator.click_button(btn_text)

        with allure.step("4. Дождаться появления результата '15'"):
            calculator.wait_for_result("15", 45)

        with allure.step("5. Получить результат и выполнить проверку"):
            result = calculator.get_result_text()
            assert result == "15", (
                f"Ошибка: ожидался результат '15', но получено '{result}'"
            )
