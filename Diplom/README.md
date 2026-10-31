# YouGile QA Automation

Автоматизированные проверки веб-приложения YouGile: API на `requests` и UI на Selenium. Отчётность — Allure.


## Стек

- Python 3.11+
- pytest
- Requests
- Selenium (Chrome для текущей UI-фикстуры)
- Allure Pytest
- python-dotenv

## Установка

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Для запуска нужен установленный Google Chrome (драйвер подбирается автоматически через Selenium Manager). Текущий автопрогон использует Chrome; кросс-браузерный чек-лист выполняется вручную.

## Настройка учётной записи

1. Укажите тестовые значения `YOUGILE_LOGIN` и `YOUGILE_PASSWORD`, в `.env.example` в `.env`.
2. Проверьте `company_name` в `config/config.ini`: значение должно совпадать с названием компании, доступной аккаунту.
3. Не коммитьте `.env` и `.env.example`, токены или реальные учётные данные.

## Запуск тестов

```bash
# Только UI
pytest -m ui

# Только API
pytest -m api

# Все тесты
pytest

# Сбор результатов Allure
pytest --alluredir=allure-results
allure serve allure-results
```

Команда `allure serve` требует установленный Allure Commandline.

## Структура

```text
config/       # конфигурация URL, компании и таймаута
data/         # тестовые данные и генераторы
 tests/api/   # API-тесты и фикстуры
 tests/ui/    # UI-тесты и Page Objects
utils/        # API-клиент
```
## Отчет 

Можно посмотреть готовый отчет, нужно выполнить python -m http.server 8000, и открыть index.html в allure-report, или составить свой после прогона тестов