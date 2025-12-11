import sys
from typing import Any, Dict, List

from src.external_api import get_transaction_amount_rub
from src.file_reader import read_csv_file, read_excel_file
from src.generators import filter_by_currency
from src.operations_analiz import count_transactions_by_category, search_transactions_by_description
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card


def load_transactions_by_format() -> List[Dict[str, Any]]:
    """Загружает транзакции в выбранном формате."""
    print("\nВыберите формат файла:")
    print("1. JSON-файл")
    print("2. CSV-файл")
    print("3. XLSX-файл")

    while True:
        try:
            choice = input("Введите номер (1-3): ").strip()

            if choice == "1":
                print("\nДля обработки выбран JSON-файл.")
                return load_transactions("data/operations.json")
            elif choice == "2":
                print("\nДля обработки выбран CSV-файл.")
                return read_csv_file("data/transactions.csv")
            elif choice == "3":
                print("\nДля обработки выбран XLSX-файл.")
                return read_excel_file("data/transactions_excel.xlsx")
            else:
                print("Пожалуйста, введите число от 1 до 3")
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return []


def filter_by_status_interactive(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по статусу с интерактивным вводом."""
    available_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\nВведите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(available_statuses)}")

        status = input("Статус: ").strip().upper()

        if status in available_statuses:
            print(f'\nОперации отфильтрованы по статусу "{status}"')
            return filter_by_state(transactions, status)
        else:
            print(f'Статус операции "{status}" недоступен.')


def sort_transactions_interactive(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Сортирует транзакции по дате с интерактивным вводом."""
    while True:
        answer = input("\nОтсортировать операции по дате? (Да/Нет): ").strip().lower()

        if answer in ["да", "yes", "y", "д"]:
            while True:
                order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()

                if "возрастан" in order or "увелич" in order:
                    print("Сортировка по возрастанию даты")
                    return sort_by_date(transactions, reverse=False)
                elif "убыван" in order or "уменьш" in order:
                    print("Сортировка по убыванию даты")
                    return sort_by_date(transactions, reverse=True)
                else:
                    print("Пожалуйста, укажите 'по возрастанию' или 'по убыванию'")
        elif answer in ["нет", "no", "n", "н"]:
            print("Сортировка не применяется")
            return transactions
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")


def filter_ruble_transactions_interactive(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует рублевые транзакции с интерактивным вводом."""
    while True:
        answer = input("\nВыводить только рублевые транзакции? (Да/Нет): ").strip().lower()

        if answer in ["да", "yes", "y", "д"]:
            print("Фильтрация по рублевым транзакциям")
            ruble_transactions = []

            for transaction in transactions:
                operation_amount = transaction.get("operationAmount", {})
                currency = operation_amount.get("currency", {}).get("code", "RUB")

                if currency == "RUB":
                    ruble_transactions.append(transaction)

            return ruble_transactions
        elif answer in ["нет", "no", "n", "н"]:
            print("Фильтрация по валюте не применяется")
            return transactions
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")


def filter_by_keyword_interactive(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрует транзакции по ключевому слову с интерактивным вводом."""
    while True:
        answer = (
            input("\nОтфильтровать список транзакций по определенному слову в описании? (Да/Нет): ").strip().lower()
        )

        if answer in ["да", "yes", "y", "д"]:
            keyword = input("Введите слово для поиска в описании: ").strip()

            if keyword:
                print(f"Поиск транзакций с ключевым словом: '{keyword}'")
                return search_transactions_by_description(transactions, keyword)
            else:
                print("Не указано ключевое слово. Фильтрация не применяется.")
                return transactions
        elif answer in ["нет", "no", "n", "н"]:
            print("Фильтрация по ключевому слову не применяется")
            return transactions
        else:
            print("Пожалуйста, ответьте 'Да' или 'Нет'")


def format_transaction_for_display(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для отображения."""
    lines = []

    # Дата
    date = get_date(transaction.get("date", ""))
    lines.append(f"{date}")

    # Описание
    description = transaction.get("description", "")
    lines.append(f"{description}")

    # Откуда и куда
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    if from_account and to_account:
        masked_from = mask_account_card(from_account)
        masked_to = mask_account_card(to_account)
        lines.append(f"{masked_from} -> {masked_to}")
    elif from_account:
        masked_from = mask_account_card(from_account)
        lines.append(f"{masked_from}")
    elif to_account:
        masked_to = mask_account_card(to_account)
        lines.append(f"-> {masked_to}")
    else:
        lines.append("Источник/назначение не указано")

    # Сумма
    amount_rub = get_transaction_amount_rub(transaction)
    operation_amount = transaction.get("operationAmount", {})
    currency = operation_amount.get("currency", {}).get("code", "RUB")

    if currency == "RUB":
        lines.append(f"Сумма: {amount_rub:.2f} руб.")
    else:
        original_amount = operation_amount.get("amount", "0")
        lines.append(f"Сумма: {original_amount} {currency} ({amount_rub:.2f} руб.)")

    return "\n".join(lines)


def display_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Отображает транзакции в консоли."""
    print("\n" + "=" * 60)
    print(f"Всего банковских операций в выборке: {len(transactions)}")
    print("=" * 60)

    if not transactions:
        print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    for i, transaction in enumerate(transactions, 1):
        print(f"\n{i}. {format_transaction_for_display(transaction)}")
        print("-" * 60)


def show_category_statistics(transactions: List[Dict[str, Any]]) -> None:
    """Показывает статистику по категориям транзакций."""
    if not transactions:
        return

    # Автоматически определяем категории из описаний
    all_descriptions = set()
    for transaction in transactions:
        description = transaction.get("description", "")
        if description:
            all_descriptions.add(description)

    if all_descriptions:
        categories = list(all_descriptions)
        category_counts = count_transactions_by_category(transactions, categories)

        print("\n Статистика по категориям операций:")
        print("-" * 40)

        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"{category}: {count} операций")


def main() -> None:
    """Основная функция программы с пользовательским интерфейсом."""
    print("=" * 60)
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("=" * 60)

    try:
        # Шаг 1: Выбор формата файла
        print("\nВыберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        transactions = load_transactions_by_format()

        if not transactions:
            print("Не удалось загрузить транзакции. Программа завершена.")
            return

        print(f"Загружено {len(transactions)} транзакций")

        # Шаг 2: Фильтрация по статусу
        transactions = filter_by_status_interactive(transactions)

        if not transactions:
            print("\nНе найдено транзакций с выбранным статусом. Программа завершена.")
            return

        # Шаг 3: Сортировка по дате
        transactions = sort_transactions_interactive(transactions)

        # Шаг 4: Фильтрация по рублевым транзакциям
        transactions = filter_ruble_transactions_interactive(transactions)

        # Шаг 5: Фильтрация по ключевому слову
        transactions = filter_by_keyword_interactive(transactions)

        # Шаг 6: Отображение результатов
        print("\n" + "=" * 60)
        print("Распечатываю итоговый список транзакций...")
        print("=" * 60)

        display_transactions(transactions)

        # Шаг 7: Показать статистику
        show_category_statistics(transactions)

        print("\n" + "=" * 60)
        print("Программа завершена. Спасибо за использование!")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")
        print("Программа завершена с ошибкой.")


if __name__ == "__main__":
    main()
