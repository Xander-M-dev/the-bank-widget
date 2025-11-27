try:
    from src.widget import mask_account_card, get_date
    from src.processing import filter_by_state, sort_by_date
    from src.generators import filter_by_currency, transaction_descriptions, card_number_generator
    from src.decorators import log
    from src.utils import load_transactions
    from src.external_api import get_transaction_amount_rub

    print(" Все модули успешно импортированы")
except ImportError as e:
    print(f" Ошибка импорта: {e}")
    exit(1)


def main() -> None:
    """Демонстрация работы всех функций проекта с логированием"""
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ФУНКЦИЙ С ЛОГИРОВАНИЕМ")
    print("=" * 60)

    # Демонстрация логирования masks
    print("\n Тестирование логирования модуля masks:")
    print("-" * 40)

    test_cards = [
        "1234567812345678",
        "123",
        "1111222233334444"
    ]

    for card in test_cards:
        result = mask_account_card(f"Card {card}")
        print(f"Карта: {card} -> {result}")

    # Демонстрация логирования utils
    print("\n Тестирование логирования модуля utils:")
    print("-" * 40)

    # Валидный файл
    try:
        transactions = load_transactions("data/operations.json")
        print(f"Загружено транзакций: {len(transactions)}")
    except Exception as e:
        print(f"Ошибка загрузки transactions: {e}")
        transactions = []

    try:
        invalid_result = load_transactions("nonexistent_file.json")
        print(f"Результат загрузки несуществующего файла: {len(invalid_result)} транзакций")
    except Exception as e:
        print(f"Ошибка загрузки несуществующего файла: {e}")

    print("\n1. Функция mask_account_card:")
    print("-" * 40)

    account_examples = [
        "Visa Platinum 7000792289606361",
        "Maestro 7000792289606361",
        "Счет 73654108430135874305",
    ]

    for example in account_examples:
        result = mask_account_card(example)
        print(f"Вход:  {example}")
        print(f"Выход: {result}")

    print("\n Демонстрация завершена!")
    print(" Логи сохранены в папке logs/")
    print("   - masks.log - логи маскировки карт и счетов")
    print("   - utils.log - логи загрузки транзакций")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f" Критическая ошибка в main(): {e}")
        import traceback

        traceback.print_exc()
