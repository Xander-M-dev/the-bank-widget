import os
from typing import Any, Dict
from unittest.mock import Mock, patch

import pytest

from src.external_api import get_currency_rate, get_transaction_amount_rub


def test_get_transaction_amount_rub_rub() -> None:
    """Тест конвертации для рублевой транзакции"""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "1000.50", "currency": {"code": "RUB"}}}

    result = get_transaction_amount_rub(transaction)
    assert result == 1000.50


def test_get_transaction_amount_rub_usd() -> None:
    """Тест конвертации для USD транзакции с моком API"""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    # Мокаем функцию получения курса
    with patch("src.external_api.get_currency_rate") as mock_rate:
        mock_rate.return_value = 75.5  # курс 1 USD = 75.5 RUB
        result = get_transaction_amount_rub(transaction)

        assert result == 7550.0  # 100 * 75.5
        mock_rate.assert_called_once_with("USD")


def test_get_transaction_amount_rub_eur() -> None:
    """Тест конвертации для EUR транзакции с моком API"""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "50.00", "currency": {"code": "EUR"}}}

    with patch("src.external_api.get_currency_rate") as mock_rate:
        mock_rate.return_value = 85.0  # курс 1 EUR = 85.0 RUB
        result = get_transaction_amount_rub(transaction)

        assert result == 4250.0  # 50 * 85.0
        mock_rate.assert_called_once_with("EUR")


def test_get_transaction_amount_rub_unknown_currency() -> None:
    """Тест для неизвестной валюты"""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "100.00", "currency": {"code": "GBP"}}}  # фунты

    result = get_transaction_amount_rub(transaction)
    assert result == 100.0  # возвращается исходная сумма


def test_get_transaction_amount_rub_api_error() -> None:
    """Тест обработки ошибки API"""
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    with patch("src.external_api.get_currency_rate") as mock_rate:
        mock_rate.side_effect = Exception("API error")
        result = get_transaction_amount_rub(transaction)

        # При ошибке должна вернуться исходная сумма
        assert result == 100.0


@patch("src.external_api.requests.get")
def test_get_currency_rate_success(mock_get: Mock) -> None:
    """Тест успешного получения курса валют"""
    # Мокаем успешный ответ API
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"rates": {"RUB": 75.5}}
    mock_get.return_value = mock_response

    # Мокаем переменную окружения
    with patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"}):
        rate = get_currency_rate("USD")
        assert rate == 75.5


@patch("src.external_api.requests.get")
def test_get_currency_rate_api_error(mock_get: Mock) -> None:
    """Тест ошибки API при получении курса"""
    mock_response = Mock()
    mock_response.status_code = 401  # ошибка авторизации
    mock_get.return_value = mock_response

    with patch.dict(os.environ, {"EXCHANGE_RATE_API_KEY": "test_key"}):
        with pytest.raises(Exception, match="Ошибка API: 401"):
            get_currency_rate("USD")


def test_get_currency_rate_no_api_key() -> None:
    """Тест отсутствия API ключа"""
    # Убеждаемся, что переменная окружения не установлена
    if "EXCHANGE_RATE_API_KEY" in os.environ:
        del os.environ["EXCHANGE_RATE_API_KEY"]

    with pytest.raises(ValueError, match="API ключ не найден"):
        get_currency_rate("USD")
