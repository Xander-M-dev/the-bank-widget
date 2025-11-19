from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date


def main() -> None:
    """Демонстрация работы всех функций проекта"""
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ФУНКЦИЙ")
    print("=" * 60)

    # Покажем документацию функций
    print("\n📋 Документация функций:")
    print("-" * 40)
    print(get_mask_card_number.__doc__)
    print(get_mask_account.__doc__)

    # Тестируем mask_account_card
    print("\n1. Функция mask_account_card:")
    print("-" * 40)

    account_examples = [
        "Visa Platinum 7000792289606361",
        "Maestro 7000792289606361",
        "Счет 73654108430135874305",
        "MasterCard 1234567812345678",
        "Счет 98765432101234567890",
    ]

    for example in account_examples:
        result = mask_account_card(example)
        print(f"Вход:  {example}")
        print(f"Выход: {result}")
        print("-" * 30)

    # Тестируем get_date
    print("\n2. Функция get_date:")
    print("-" * 40)

    date_examples = [
        "2024-03-11T02:26:18.671407",
        "2023-12-25T15:30:45.123456",
        "2022-07-01T00:00:00.000000",
    ]

    for example in date_examples:
        result = get_date(example)
        print(f"Вход:  {example}")
        print(f"Выход: {result}")
        print("-" * 30)

    # Тестируем processing функции
    print("\n3. Функции обработки операций:")
    print("-" * 40)

    operations = [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:30:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-14T12:45:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-16T09:15:00.000000"},
        {"id": 4, "state": "PENDING", "date": "2024-01-13T08:00:00.000000"},
    ]

    print("Фильтрация выполненных операций:")
    executed_ops = filter_by_state(operations, "EXECUTED")
    for op in executed_ops:
        print(f"  Операция {op['id']}: {op['state']} - {get_date(op['date'])}")

    print("\nСортировка операций (новые сначала):")
    sorted_ops = sort_by_date(operations, True)
    for op in sorted_ops:
        print(f"  Операция {op['id']}: {get_date(op['date'])} - {op['state']}")


if __name__ == "__main__":
    main()
