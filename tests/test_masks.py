import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize("card_number, expected", [
    ("7000792289606361", "7000 79** **** 6361"),
    ("1234567812345678", "1234 56** **** 5678"),
    ("1111222233334444", "1111 22** **** 4444"),
])
def test_get_mask_card_number_valid(card_number, expected):
    """Тест маскировки номера карты"""
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_short():
    """Тест маскировки короткого номера карты"""
    assert get_mask_card_number("1234") == "1234"


@pytest.mark.parametrize("account_number, expected", [
    ("73654108430135874305", "**4305"),
    ("12345678901234567890", "**7890"),
    ("98765432101234567890", "**7890"),
])
def test_get_mask_account_valid(account_number, expected):
    """Тест маскировки номера счета с валидными данными"""
    assert get_mask_account(account_number) == expected


def test_get_mask_account_short():
    """Тест маскировки короткого номера счета"""
    assert get_mask_account("123") == "123"