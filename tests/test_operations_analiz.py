import pytest

from src.operations_analiz import count_transactions_by_category, search_transactions_by_description


def test_search_transactions_by_description_empty() -> None:
    """Тест поиска с пустыми данными"""
    result = search_transactions_by_description([], "test")
    assert result == []

    result = search_transactions_by_description([{"description": "test"}], "")
    assert result == []


def test_search_transactions_by_description_case_insensitive() -> None:
    """Тест поиска без учета регистра"""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод С ОРГАНИЗАЦИИ"},
        {"id": 3, "description": "Открытие вклада"},
        {"id": 4, "description": "перевод физ лицу"},
    ]

    result = search_transactions_by_description(transactions, "перевод")
    assert len(result) == 3
    assert all("перевод" in tx["description"].lower() for tx in result)


def test_search_transactions_by_description_specific() -> None:
    """Тест поиска конкретной фразы"""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
        {"id": 3, "description": "Перевод физ лицу"},
    ]

    result = search_transactions_by_description(transactions, "вклад")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_search_transactions_by_description_no_match() -> None:
    """Тест поиска без совпадений"""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Открытие вклада"},
    ]

    result = search_transactions_by_description(transactions, "карта")
    assert result == []


def test_search_transactions_by_description_special_chars() -> None:
    """Тест поиска со специальными символами"""
    transactions = [
        {"id": 1, "description": "Payment (USD) to company"},
        {"id": 2, "description": "Refund [test]"},
    ]

    result = search_transactions_by_description(transactions, "(USD)")
    assert len(result) == 1
    assert result[0]["id"] == 1


def test_count_transactions_by_category_empty() -> None:
    """Тест подсчета с пустыми данными"""
    result = count_transactions_by_category([], ["test"])
    assert result == {}

    result = count_transactions_by_category([{"description": "test"}], [])
    assert result == {}


def test_count_transactions_by_category_basic() -> None:
    """Тест базового подсчета категорий"""
    transactions = [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод организации"},
        {"id": 3, "description": "Открытие вклада"},
        {"id": 4, "description": "Перевод физ лицу"},
        {"id": 5, "description": "Открытие вклада"},
        {"id": 6, "description": "Перевод организации"},
    ]

    categories = ["Перевод", "Вклад"]
    result = count_transactions_by_category(transactions, categories)

    assert result["Перевод"] == 4  # ID: 1, 2, 4, 6
    assert result["Вклад"] == 2  # ID: 3, 5


def test_count_transactions_by_category_case_insensitive() -> None:
    """Тест подсчета без учета регистра"""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "перевод физ лицу"},
        {"description": "ПЕРЕВОД юр лицу"},
        {"description": "Открытие вклада"},
    ]

    categories = ["перевод", "вклад"]
    result = count_transactions_by_category(transactions, categories)

    assert result["перевод"] == 3
    assert result["вклад"] == 1


def test_count_transactions_by_category_partial_match() -> None:
    """Тест подсчета с частичным совпадением"""
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод между счетами"},
        {"description": "Возврат перевода"},
        {"description": "Открытие вклада"},
        {"description": "Пополнение вклада"},
    ]

    categories = ["перевод", "вклад"]
    result = count_transactions_by_category(transactions, categories)

    assert result["перевод"] == 3  # Все содержащие "перевод"
    assert result["вклад"] == 2  # Все содержащие "вклад"


def test_count_transactions_by_category_no_description() -> None:
    """Тест подсчета транзакций без описания"""
    transactions = [
        {"id": 1, "description": ""},
        {"id": 2},  # Нет ключа description
        {"id": 3, "description": "Перевод"},
    ]

    categories = ["Перевод"]
    result = count_transactions_by_category(transactions, categories)

    assert result["Перевод"] == 1


def test_count_transactions_by_category_multiple_matches() -> None:
    """Тест когда одна транзакция может попадать в несколько категорий"""
    transactions = [
        {"description": "Перевод организации на вклад"},
        {"description": "Открытие вклада"},
        {"description": "Перевод физ лицу"},
    ]

    categories = ["перевод", "вклад"]
    result = count_transactions_by_category(transactions, categories)

    # Первая транзакция попадает в обе категории
    assert result["перевод"] == 2  # ID: 1, 3
    assert result["вклад"] == 2  # ID: 1, 2
