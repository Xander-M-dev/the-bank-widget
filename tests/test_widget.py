import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "input_data, expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card_valid(input_data: str, expected: str) -> None:
    """Тест маскировки карт и счетов с валидными данными"""
    assert mask_account_card(input_data) == expected


def test_mask_account_card_empty() -> None:
    """Тест маскировки с пустыми данными"""
    assert mask_account_card("") == " "


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-25T15:30:45.123456", "25.12.2023"),
        ("2022-07-01T00:00:00.000000", "01.07.2022"),
    ],
)
def test_get_date_valid(date_string: str, expected: str) -> None:
    """Тест форматирования даты с валидными данными"""
    assert get_date(date_string) == expected
