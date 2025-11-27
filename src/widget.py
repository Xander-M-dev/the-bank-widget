from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа."""
    if not account_info or account_info.strip() == "":
        return " "

    parts = account_info.split()

    if len(parts) < 2:
        return account_info

    number = parts[-1]

    account_type = " ".join(parts[:-1])

    if "счет" in account_type.lower():
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """Преобразует дату из формата "2024-03-11T02:26:18.671407" в "11.03.2024"."""
    try:
        dt = datetime.fromisoformat(date_string)

        return dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return "Неверный формат даты"
