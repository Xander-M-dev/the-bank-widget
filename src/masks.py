from .logging_config import setup_logging

# Настраиваем логгер для модуля masks
logger = setup_logging("masks")


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты, оставляя первые 6 и последние 4 цифры."""
    try:
        logger.debug(f"Начало маскировки номера карты: {card_number}")

        if len(card_number) != 16 or not card_number.isdigit():
            error_msg = f"Неверный формат номера карты: {card_number}. Ожидается 16 цифр"
            logger.error(error_msg)
            return card_number

        masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.debug(f"Номер карты успешно замаскирован: {masked_number}")
        return masked_number

    except Exception as e:
        error_msg = f"Ошибка при маскировке номера карты {card_number}: {str(e)}"
        logger.error(error_msg)
        return card_number


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета, оставляя только последние 4 цифры."""
    try:
        logger.debug(f"Начало маскировки номера счета: {account_number}")

        if len(account_number) < 4 or not account_number.isdigit():
            error_msg = f"Неверный формат номера счета: {account_number}. Ожидается минимум 4 цифры"
            logger.error(error_msg)
            return account_number

        masked_number = f"**{account_number[-4:]}"
        logger.debug(f"Номер счета успешно замаскирован: {masked_number}")
        return masked_number

    except Exception as e:
        error_msg = f"Ошибка при маскировке номера счета {account_number}: {str(e)}"
        logger.error(error_msg)
        return account_number
