"""Модуль для анализа банковских операций с использованием регулярных выражений и подсчета категорий."""

import re
from collections import Counter
from typing import Any, Dict, List


def search_transactions_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """Ищет транзакции по заданной строке в описании с использованием регулярных выражений."""
    try:
        if not transactions or not search_string:
            return []

        # Используем регулярное выражение для поиска без учета регистра
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)
        result = []

        for transaction in transactions:
            description = transaction.get("description", "")
            if description and pattern.search(description):
                result.append(transaction)

        return result

    except Exception as e:
        print(f"Ошибка при поиске транзакций: {e}")
        return []


def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество операций по заданным категориям."""
    try:
        if not transactions or not categories:
            return {}

        # Получаем все описания транзакций
        descriptions = []
        for transaction in transactions:
            description = transaction.get("description", "").strip()
            if description:
                descriptions.append(description)

        # Используем Counter для подсчета
        description_counter = Counter(descriptions)

        # Фильтруем только нужные категории
        result = {}
        for category in categories:
            # Ищем совпадения без учета регистра
            category_lower = category.lower()
            count = 0

            for description, desc_count in description_counter.items():
                if category_lower in description.lower():
                    count += desc_count

            result[category] = count

        return result

    except Exception as e:
        print(f"Ошибка при подсчете транзакций: {e}")
        return {}
