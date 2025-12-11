from pathlib import Path
from unittest.mock import MagicMock, patch

from src.file_reader import read_csv_file, read_excel_file


def test_read_csv_file_success() -> None:
    """Тест успешного чтения CSV файла"""
    # Мокаем pandas.read_csv и Path.exists
    with patch("pathlib.Path.exists") as mock_exists:
        with patch("pandas.read_csv") as mock_read_csv:
            # Настраиваем моки
            mock_exists.return_value = True
            mock_df = MagicMock()
            mock_df.to_dict.return_value = [
                {"id": 1, "amount": 100.50, "currency": "USD", "description": "Test transaction 1"},
                {"id": 2, "amount": 200.75, "currency": "EUR", "description": "Test transaction 2"},
            ]
            mock_read_csv.return_value = mock_df

            # Вызываем тестируемую функцию
            result = read_csv_file("test.csv")

            # Проверяем результаты
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["currency"] == "EUR"
            mock_read_csv.assert_called_once_with("test.csv")


def test_read_csv_file_not_found() -> None:
    """Тест чтения несуществующего CSV файла"""
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = False

        result = read_csv_file("nonexistent.csv")
        assert result == []


def test_read_csv_file_exception() -> None:
    """Тест обработки исключения при чтении CSV"""
    with patch("pathlib.Path.exists") as mock_exists:
        with patch("pandas.read_csv") as mock_read_csv:
            mock_exists.return_value = True
            mock_read_csv.side_effect = Exception("Test error")

            result = read_csv_file("test.csv")
            assert result == []


def test_read_excel_file_success() -> None:
    """Тест успешного чтения Excel файла"""
    with patch("pathlib.Path.exists") as mock_exists:
        with patch("pandas.read_excel") as mock_read_excel:
            # Настраиваем моки
            mock_exists.return_value = True
            mock_df = MagicMock()
            mock_df.to_dict.return_value = [
                {"id": 1, "amount": 150.25, "currency": "RUB", "description": "Excel transaction 1"},
                {"id": 2, "amount": 300.00, "currency": "USD", "description": "Excel transaction 2"},
            ]
            mock_read_excel.return_value = mock_df

            # Вызываем тестируемую функцию
            result = read_excel_file("test.xlsx")

            # Проверяем результаты
            assert len(result) == 2
            assert result[0]["amount"] == 150.25
            assert result[1]["description"] == "Excel transaction 2"
            mock_read_excel.assert_called_once_with("test.xlsx")


def test_read_excel_file_not_found() -> None:
    """Тест чтения несуществующего Excel файла"""
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = False

        result = read_excel_file("nonexistent.xlsx")
        assert result == []


def test_read_excel_file_exception() -> None:
    """Тест обработки исключения при чтении Excel"""
    with patch("pathlib.Path.exists") as mock_exists:
        with patch("pandas.read_excel") as mock_read_excel:
            mock_exists.return_value = True
            mock_read_excel.side_effect = Exception("Test error")

            result = read_excel_file("test.xlsx")
            assert result == []


def test_read_csv_file_integration() -> None:
    """Тест с  CSV файлом"""
    test_file = Path("data/transactions.csv")
    if test_file.exists():
        result = read_csv_file("data/transactions.csv")
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], dict)


def test_read_excel_file_integration() -> None:
    """Тест с Excel файлом"""
    test_file = Path("data/transactions_excel.xlsx")
    if test_file.exists():
        result = read_excel_file("data/transactions_excel.xlsx")
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], dict)
