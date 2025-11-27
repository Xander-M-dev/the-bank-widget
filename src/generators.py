from typing import Any, Dict, Iterator


def filter_by_currency(transactions: list[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Фильтрует транзакции по валюте и возвращает итератор"""
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency_code = operation_amount.get("currency", {}).get("code")
        if currency_code == currency:
            yield transaction


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    """Генератор, который возвращает описание каждой операции по очереди"""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Генератор номеров банковских карт в заданном диапазоне"""
    for number in range(start, end + 1):
        card_str = str(number).zfill(16)
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        yield formatted_card
