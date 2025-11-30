# The Bank Widget - Виджет для банка

Проект для работы с банковскими операциями: маскировка карт, форматирование дат, фильтрация операций.

## Установка

1. Скачай проект:

git clone https://github.com/Xander-M-dev/the-bank-widget.git
cd the-bank-widget


## Линтеры

ini
[flake8]
max-line-length = 119
extend-ignore = E203, W503, E501
Black (файл pyproject.toml):

toml
[tool.black]
line-length = 119
exclude = '\.git'
isort (файл pyproject.toml):

toml
[tool.isort]
line_length = 119
multi_line_output = 3
mypy (файл pyproject.toml):

toml
[tool.mypy]
disallow_untyped_defs = true
warn_return_any = true


# Проверка качества кода


### Форматирование кода
poetry run black .

### Сортировка импортов
poetry run isort .

### Проверка стиля
poetry run flake8 .

### Проверка типов
poetry run mypy .

## Как использовать
### Спрятать номер карты или счёта
python
from src.widget import mask_account_card

### Для карт
print(mask_account_card("Visa Platinum 7000792289606361"))
### Напечатает: Visa Platinum 7000 79** **** 6361

### Для счетов  
print(mask_account_card("Счет 73654108430135874305"))
### Напечатает: Счет **4305

### Дата
python
from src.widget import get_date
print(get_date("2024-03-11T02:26:18.671407"))
### Напечатает: 11.03.2024

## Отфильтровать операции
python
from src.processing import filter_by_state

operations = [
    {"id": 1, "state": "EXECUTED", "date": "2024-01-15"},
    {"id": 2, "state": "CANCELED", "date": "2024-01-14"},
]

## Показать только выполненные операции
result = filter_by_state(operations)
print(result)  # Покажет только операцию 1
Отсортировать по дате
python
from src.processing import sort_by_date

### Сначала новые
new_first = sort_by_date(operations)

### Сначала старые  
old_first = sort_by_date(operations, False)

## Генераторы данных

Модуль `generators` предоставляет инструменты для эффективной работы с большими объемами данных транзакций.

### Фильтрация транзакций по валюте
python
from src.generators import filter_by_currency

transactions = [...]  # ваш список транзакций
usd_transactions = filter_by_currency(transactions, "USD")

### Использование как итератора
for transaction in usd_transactions:
    print(transaction)

### Или с помощью next()
usd_iter = filter_by_currency(transactions, "USD")
print(next(usd_iter))
print(next(usd_iter))


## Для разработчиков
Структура проекта
text
the-bank-widget/
├── src/
│   ├── masks.py       # Прячет цифры карт и счетов
│   ├── widget.py      # Основные функции
│   └── processing.py  # Сортировка и фильтрация
├── tests/
├── main.py            # Примеры использования
├── pyproject.toml     # Конфигурация и зависимости
├── .flake8           # Настройки Flake8
└── README.md          # Эта инструкция
Зависимости проекта
Основные: Python 3.8+

Для разработки: flake8, black, isort, mypy

Менеджер пакетов: Poetry

Быстрый старт
bash
git clone https://github.com/Xander-M-dev/the-bank-widget.git
cd the-bank-widget
poetry install
poetry install --with lint
poetry shell
python main.py

# Тесты
poetry run pytest

## С подробным выводом
poetry run pytest -v

## С покрытием кода
poetry run pytest --cov=src

## Генерация HTML отчета покрытия
poetry run pytest --cov=src --cov-report=html

#  Декораторы

Модуль "decorators" предоставляет инструменты для автоматического логирования выполнения функций.

## Декоратор log
Автоматически логирует начало и конец выполнения функции, а также ошибки.


from src.decorators import log

### Логирование в консоль
@log()
def add(a: int, b: int) -> int:
    return a + b
### Логирование в файл
@log(filename="operations.log")
def divide(a: int, b: int) -> float:
    return a / b

#  Чтение CSV и Excel файлов

Модуль file_reader предоставляет функции для чтения транзакций из различных форматов:

## Чтение CSV файлов

python
from src.file_reader import read_csv_file

transactions = read_csv_file("data/transactions.csv")
print(f"Загружено {len(transactions)} транзакций")
