import pytest
import os
from typing import Dict, Any
from unittest.mock import patch, Mock
from src.external_api import convert_currency, get_transaction_amount_rub


def test_convert_currency_success() -> None:
    """Тест успешной конвертации валюты"""
    # Мокаем успешный ответ API для endpoint /convert
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'success': True,
        'result': 7500.0  # 100 USD = 7500 RUB
    }

    with patch('src.external_api.requests.get') as mock_get:
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            result = convert_currency(100.0, 'USD', 'RUB')
            assert result == 7500.0

            # Проверяем что запрос был к правильному endpoint
            mock_get.assert_called_once()
            call_args = mock_get.call_args[0][0]
            assert 'convert' in call_args
            assert 'from=USD' in call_args
            assert 'to=RUB' in call_args
            assert 'amount=100' in call_args


def test_convert_currency_api_error() -> None:
    """Тест ошибки API при конвертации"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = {
        'success': False,
        'error': {'info': 'Invalid API Key'}
    }

    with patch('src.external_api.requests.get') as mock_get:
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            with pytest.raises(Exception, match="Ошибка API: 401"):
                convert_currency(100.0, 'USD', 'RUB')


def test_convert_currency_no_result() -> None:
    """Тест ответа API без поля result"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'success': True
        # Нет поля 'result'
    }

    with patch('src.external_api.requests.get') as mock_get:
        mock_get.return_value = mock_response

        with patch.dict(os.environ, {'EXCHANGE_RATE_API_KEY': 'test_key'}):
            with pytest.raises(Exception, match="Ошибка в ответе API"):
                convert_currency(100.0, 'USD', 'RUB')


def test_get_transaction_amount_rub_usd_conversion() -> None:
    """Тест конвертации USD транзакции через API convert"""
    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    # Мокаем функцию convert_currency
    with patch('src.external_api.convert_currency') as mock_convert:
        mock_convert.return_value = 7500.0  # 100 USD = 7500 RUB
        result = get_transaction_amount_rub(transaction)

        assert result == 7500.0
        mock_convert.assert_called_once_with(100.0, 'USD', 'RUB')


def test_get_transaction_amount_rub_eur_conversion() -> None:
    """Тест конвертации EUR транзакции через API convert"""
    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "50.00",
            "currency": {
                "code": "EUR"
            }
        }
    }

    with patch('src.external_api.convert_currency') as mock_convert:
        mock_convert.return_value = 5000.0  # 50 EUR = 5000 RUB
        result = get_transaction_amount_rub(transaction)

        assert result == 5000.0
        mock_convert.assert_called_once_with(50.0, 'EUR', 'RUB')


# Остальные тесты остаются без изменений...
def test_get_transaction_amount_rub_rub() -> None:
    """Тест конвертации для рублевой транзакции"""
    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "1000.50",
            "currency": {
                "code": "RUB"
            }
        }
    }

    result = get_transaction_amount_rub(transaction)
    assert result == 1000.50


def test_get_transaction_amount_rub_unknown_currency() -> None:
    """Тест для неизвестной валюты"""
    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "GBP"  # фунты
            }
        }
    }

    result = get_transaction_amount_rub(transaction)
    assert result == 100.0


def test_get_transaction_amount_rub_api_error() -> None:
    """Тест обработки ошибки API"""
    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "USD"
            }
        }
    }

    with patch('src.external_api.convert_currency') as mock_convert:
        mock_convert.side_effect = Exception("API error")
        result = get_transaction_amount_rub(transaction)

        # При ошибке должна вернуться исходная сумма
        assert result == 100.0


def test_convert_currency_no_api_key() -> None:
    """Тест отсутствия API ключа"""
    # Убеждаемся, что переменная окружения не установлена
    if 'EXCHANGE_RATE_API_KEY' in os.environ:
        del os.environ['EXCHANGE_RATE_API_KEY']

    with pytest.raises(ValueError, match="API ключ не найден"):
        convert_currency(100.0, 'USD', 'RUB')
