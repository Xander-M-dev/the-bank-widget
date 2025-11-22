import json
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные - это список
        if isinstance(data, list):
            return data
        else:
            return []

    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или ошибка JSON - возвращаем пустой список
        return []
    except Exception:
        # Любая другая ошибка - тоже возвращаем пустой список
        return []
