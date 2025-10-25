def get_mask_card_number(number_card: str) -> str:
    """принимает на вход номер карты и возвращает ее маску"""
    card_number_str = number_card.replace(" ", "")
    return card_number_str[:5] + " " + card_number_str[5:7] + "** **** " + card_number_str[-4:]


def get_mask_account(number_chek: str) -> str:
    """принимает на вход номер счета и возвращает его маску"""
    return "**" + number_chek[-4:]
