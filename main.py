from src.masks import get_mask_card_number, get_mask_account

if __name__ == "__main__":
    print(get_mask_card_number.__doc__)
    print(get_mask_account.__doc__)
from src.widget import mask_account_card

# Примеры использования
print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361
print(mask_account_card("Maestro 7000792289606361"))  # Maestro 7000 79** **** 6361
print(mask_account_card("Счет 73654108430135874305"))  # Счет **4305

from src.widget import mask_account_card


def main() -> None:
    """Примеры использования функции mask_account_card"""
    examples = [
        "Visa Platinum 7000792289606361",
        "Maestro 7000792289606361",
        "Счет 73654108430135874305",
        "MasterCard 1234567812345678",
        "Счет 98765432101234567890",
    ]

    print("Демонстрация работы функции mask_account_card:")
    print("=" * 50)

    for example in examples:
        result = mask_account_card(example)
        print(f"Вход:  {example}")
        print(f"Выход: {result}")
        print("-" * 30)


if __name__ == "__main__":
    main()

from src.widget import get_date

print("\nДемонстрация работы функции get_date:")
print("=" * 50)

date_examples = ["2024-03-11T02:26:18.671407", "2023-12-25T15:30:45.123456", "2022-07-01T00:00:00.000000"]

for example in date_examples:
    result = get_date(example)
    print(f"Вход:  {example}")
    print(f"Выход: {result}")
    print("-" * 30)
