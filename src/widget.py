from .masks import get_mask_account, get_mask_card_number
from datetime import datetime


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа"""

    parts = account_info.split()

    number = parts[-1]

    account_type = " ".join(parts[:-1])

    if "номер счёта" in account_type.lower():
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """Преобразует дату из формата "2024-03-11T02:26:18.671407" в "11.03.2024"."""

    # Преобразуем строку в объект datetime
    dt = datetime.fromisoformat(date_string)

    # Форматируем в нужный формат
    return dt.strftime("%d.%m.%Y")
