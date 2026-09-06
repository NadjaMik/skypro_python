# Lesson 10 — Allure + PageObject

> Домашнее задание по доработке проекта из **lesson_7** с добавлением **Allure-отчётности**, **типизации** и **документирования** кода.

---

## 📁 Структура проекта

```text
lesson_10/
├── pages/                      # Page Object классы
│   ├── __init__.py
│   ├── calculator_page.py      # Страница калькулятора
│   ├── login_page.py           # Страница авторизации
│   ├── inventory_page.py       # Каталог товаров
│   ├── cart_page.py            # Корзина
│   └── checkout_page.py        # Оформление заказа
├── tests/                      # Автотесты
│   ├── __init__.py
│   ├── test_calc.py            # Тест калькулятора
│   └── test_shop.py            # E2E-тест магазина
├── conftest.py                 # Фикстуры pytest (WebDriver)
├── pytest.ini                  # Конфигурация pytest
├── requirements.txt            # Зависимости проекта
├── .gitignore                  # Исключения для Git
└── README.md                   # Документация (этот файл)
```

---

## 🚀 Установка и настройка

### 1. Установка зависимостей

Перед первым запуском установите все необходимые пакеты:

```bash
pip install -r requirements.txt
```

> **Примечание:** `webdriver-manager` автоматически скачает актуальную версию ChromeDriver.

---

## ▶️ Запуск тестов

### Запуск всех тестов с формированием Allure-результатов

```bash
pytest
```

Или явно с указанием директории результатов:

```bash
pytest --alluredir=allure-results
```

После выполнения в папке `allure-results/` появятся JSON-файлы с данными о прогоне.

---

## 📊 Просмотр Allure-отчёта

### Вариант 1. Временный просмотр (рекомендуется)

Команда `allure serve` генерирует отчёт «на лету», открывает его в браузере и **не сохраняет** HTML-файлы в проекте:

```bash
allure serve allure-results
```

### Вариант 2. Генерация статического отчёта

Если нужно сохранить HTML-отчёт локально:

```bash
# 1. Сгенерировать HTML-отчёт в папку allure-report
allure generate allure-results -o allure-report --clean

# 2. Открыть отчёт в браузере
allure open allure-report
```

> **Важно:** папки `allure-results/` и `allure-report/` добавлены в `.gitignore` и **не должны попадать в Git**.

---

## 🏷️ Allure-разметка в проекте

| Элемент | Где используется | Пример |
|---------|------------------|--------|
| `@allure.feature` | Класс тестов | `@allure.feature("Интернет-магазин SauceDemo")` |
| `@allure.title` | Метод теста | `@allure.title("Успешное оформление заказа")` |
| `@allure.description` | Метод теста | `@allure.description("Авторизуемся, добавляем 3 товара...")` |
| `@allure.severity` | Класс / метод | `@allure.severity(allure.severity_level.CRITICAL)` |
| `@allure.step` | Методы Page | `@allure.step("Открыть страницу авторизации")` |
| `with allure.step(...)` | Шаги внутри теста | `with allure.step("1. Авторизация"):` |

---

## 📝 Типизация и документация

Все методы классов `Page` содержат:

- **Аннотации типов** параметров (кроме `self`);
- **Аннотации типов** возвращаемых значений (`-> None`, `-> str` и т.д.);
- **Docstrings** с описанием назначения и параметров.

---

## ⚠️ Правила работы с Git

Папки с результатами тестов и сгенерированные отчёты **не пушатся**:

- `allure-results/` — сырые данные прогона;
- `allure-report/` — сгенерированный HTML-отчёт.

Они уже указаны в `.gitignore`. При необходимости можно закоммитить **пустую** папку `allure-results/` как заглушку:

```bash
mkdir allure-results
touch allure-results/.gitkeep
git add allure-results/.gitkeep
```

---

## 📚 Полезные ссылки

- [Синтаксис Markdown на GitHub](https://docs.github.com/ru/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [Документация Allure](https://docs.qameta.io/allure/)
- [Документация pytest](https://docs.pytest.org/)
