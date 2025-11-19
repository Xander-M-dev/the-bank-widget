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

    return None  # Явно возвращаем None


if __name__ == "__main__":
    main()
