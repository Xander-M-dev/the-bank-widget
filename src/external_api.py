import os
import requests
from typing import Dict, Any


def convert_currency(amount: float, from_currency: str, to_currency: str = "RUB") -> float:
    """Конвертирует сумму из одной валюты в другую через API."""
    # Получаем API ключ из переменных окружения
    api_key = os.getenv('EXCHANGE_RATE_API_KEY')

    if not api_key:
        raise ValueError("API ключ не найден. Проверьте переменную окружения EXCHANGE_RATE_API_KEY")

    # Используем endpoint /convert как требуется
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"

    try:
        # Делаем запрос к API
        response = requests.get(
            url,
            headers={"apikey": api_key},
            timeout=10
        )

        if response.status_code == 200:
            data: Dict[str, Any] = response.json()

            # Проверяем успешность запроса и наличие поля result
            if data.get('success') and 'result' in data:
                return float(data['result'])
            else:
                error_info = data.get('error', {}).get('info', 'Неизвестная ошибка API')
                raise Exception(f"Ошибка в ответе API: {error_info}")
        else:
            raise Exception(f"Ошибка API: {response.status_code}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка сети: {e}")


def get_transaction_amount_rub(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли."""
    try:
        # Получаем информацию о сумме и валюте
        operation_amount = transaction.get('operationAmount', {})
        amount_str = operation_amount.get('amount', '0')
        currency = operation_amount.get('currency', {}).get('code', 'RUB')

        # Конвертируем строку в float
        amount = float(amount_str)

        # Если валюта уже рубли - возвращаем как есть
        if currency == 'RUB':
            return amount

        # Если валюта USD или EUR - конвертируем через API
        if currency in ['USD', 'EUR']:
            try:
                # Используем API для конвертации, полагаясь на результат от API
                return convert_currency(amount, currency, "RUB")
            except Exception as e:
                print(f"Ошибка конвертации валюты {currency}: {e}")
                return amount

        # Для других валют возвращаем исходную сумму
        return amount

    except (ValueError, KeyError) as e:
        print(f"Ошибка обработки транзакции: {e}")
        return 0.0
