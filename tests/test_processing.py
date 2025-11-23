import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_operations() -> list[dict]:
    """Фикстура с тестовыми данными операций"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:30:00.000000"},
        {"id": 2, "state": "CANCELED", "date": "2024-01-14T12:45:00.000000"},
        {"id": 3, "state": "EXECUTED", "date": "2024-01-16T09:15:00.000000"},
    ]


def test_filter_by_state_executed(sample_operations: list[dict]) -> None:
    """Тест фильтрации по статусу EXECUTED"""
    result = filter_by_state(sample_operations, "EXECUTED")
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


def test_filter_by_state_canceled(sample_operations: list[dict]) -> None:
    """Тест фильтрации по статусу CANCELED"""
    result = filter_by_state(sample_operations, "CANCELED")
    assert len(result) == 1
    assert result[0]["state"] == "CANCELED"


def test_filter_by_state_default(sample_operations: list[dict]) -> None:
    """Тест фильтрации со статусом по умолчанию"""
    result = filter_by_state(sample_operations)
    assert len(result) == 2
    assert all(op["state"] == "EXECUTED" for op in result)


def test_sort_by_date_descending(sample_operations: list[dict]) -> None:
    """Тест сортировки по убыванию даты"""
    result = sort_by_date(sample_operations, True)
    dates = [op["date"] for op in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_operations: list[dict]) -> None:
    """Тест сортировки по возрастанию даты"""
    result = sort_by_date(sample_operations, False)
    dates = [op["date"] for op in result]
    assert dates == sorted(dates)


def test_sort_by_date_default(sample_operations: list[dict]) -> None:
    """Тест сортировки с порядком по умолчанию"""
    result = sort_by_date(sample_operations)
    dates = [op["date"] for op in result]
    assert dates == sorted(dates, reverse=True)
