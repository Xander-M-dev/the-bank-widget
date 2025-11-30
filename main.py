from src.decorators import log
from src.external_api import get_transaction_amount_rub
from src.file_reader import read_csv_file, read_excel_file
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions
from src.widget import get_date, mask_account_card


def main() -> None:
    """Демонстрация работы всех функций проекта"""
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ФУНКЦИЙ THE BANK WIDGET")
    print("=" * 60)

    # Демонстрация логирования masks
    print("\n Тестирование логирования модуля masks:")
    print("-" * 40)

    test_cards = ["1234567812345678", "123", "1111222233334444"]

    for card in test_cards:
        result = mask_account_card(f"Card {card}")
        print(f"Карта: {card} -> {result}")

    # Демонстрация логирования utils
    print("\n Тестирование логирования модуля utils:")
    print("-" * 40)

    # Валидный файл
    transactions = load_transactions("data/operations.json")
    print(f"Загружено транзакций из JSON: {len(transactions)}")

    # Невалидный файл
    invalid_result = load_transactions("nonexistent_file.json")
    print(f"Результат загрузки несуществующего файла: {len(invalid_result)} транзакций")

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

    # Тестируем генераторы
    print("\n4. Генераторы:")
    print("-" * 40)

    sample_transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]

    print("Фильтрация транзакций по USD:")
    for transaction in filter_by_currency(sample_transactions, "USD"):
        amount = transaction["operationAmount"]["amount"]
        print(f"  {amount} USD - {transaction['description']}")

    print("\nОписания транзакций:")
    for description in transaction_descriptions(sample_transactions):
        print(f"  - {description}")

    print("\nГенератор номеров карт (1-5):")
    for card_number in card_number_generator(1, 5):
        print(f"  {card_number}")

    # Тестируем декоратор
    print("\n5. Декоратор log:")
    print("-" * 40)

    @log()
    def decorated_add(a: int, b: int) -> int:
        return a + b

    @log()
    def decorated_divide(a: int, b: int) -> float:
        return a / b

    print("Логирование успешной операции:")
    result = decorated_add(10, 20)
    print(f"  Результат: {result}")

    print("Логирование операции с ошибкой:")
    try:
        decorated_divide(10, 0)
    except ZeroDivisionError:
        print("  Ошибка перехвачена и залогирована")

    # Демонстрация конвертации валют
    print("\n6. Конвертация валют:")
    print("-" * 40)

    # Загрузка транзакций из файла
    loaded_transactions = load_transactions("data/operations.json")
    print(f"Загружено транзакций: {len(loaded_transactions)}")

    if loaded_transactions:
        # Показываем первые 3 транзакции
        for i, transaction in enumerate(loaded_transactions[:3]):
            print(f"\nТранзакция {i + 1}:")
            print(f"  Описание: {transaction.get('description', 'N/A')}")

            # Получаем сумму в рублях
            amount_rub = get_transaction_amount_rub(transaction)
            operation_amount = transaction.get("operationAmount", {})
            original_amount = operation_amount.get("amount", "N/A")
            currency = operation_amount.get("currency", {}).get("code", "N/A")

            print(f"  Сумма: {original_amount} {currency}")
            print(f"  Сумма в рублях: {amount_rub:.2f} RUB")

    # Демонстрация новых функций (CSV и Excel)
    print("\n7. Чтение CSV и Excel файлов:")
    print("-" * 40)

    # Чтение CSV файла
    csv_transactions = read_csv_file("data/transactions.csv")
    print(f"Загружено транзакций из CSV: {len(csv_transactions)}")

    # Чтение Excel файла
    excel_transactions = read_excel_file("data/transactions_excel.xlsx")
    print(f"Загружено транзакций из Excel: {len(excel_transactions)}")

    # Показываем примеры данных
    if csv_transactions:
        print(f"\nПример транзакции из CSV:")
        first_tx = csv_transactions[0]
        for key, value in list(first_tx.items())[:3]:  # Показываем первые 3 поля
            print(f"  {key}: {value}")

    if excel_transactions:
        print(f"\nПример транзакции из Excel:")
        first_tx = excel_transactions[0]
        for key, value in list(first_tx.items())[:3]:  # Показываем первые 3 поля
            print(f"  {key}: {value}")

    print("\n Логи сохранены в папке logs/")
    print("   - masks.log - логи маскировки карт и счетов")
    print("   - utils.log - логи загрузки транзакций")
    print("\n Демонстрация завершена!")


if __name__ == "__main__":
    main()
