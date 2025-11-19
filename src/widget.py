from .masks import get_mask_account, get_mask_card_number


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
