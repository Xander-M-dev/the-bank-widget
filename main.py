from src.masks import get_mask_card_number, get_mask_account

if __name__ == "__main__":
    print(get_mask_card_number.__doc__)
    print(get_mask_account.__doc__)
from src.widget import mask_account_card

# Примеры использования
print(mask_account_card("Visa Platinum 7000792289606361"))  # Visa Platinum 7000 79** **** 6361
print(mask_account_card("Maestro 7000792289606361"))        # Maestro 7000 79** **** 6361
print(mask_account_card("Счет 73654108430135874305"))       # Счет **4305