import json
from typing import Any, Dict, List

from .logging_config import setup_logging

# Настраиваем логгер для модуля utils
logger = setup_logging("utils")


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает транзакции из JSON-файла."""
    try:
        logger.debug(f"Начало загрузки транзакций из файла: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Проверяем, что данные - это список
        if isinstance(data, list):
            logger.info(f"Успешно загружено {len(data)} транзакций из файла {file_path}")
            return data
        else:
            warning_msg = f"Файл {file_path} не содержит список. Возвращен пустой список"
            logger.warning(warning_msg)
            return []

    except FileNotFoundError:
        error_msg = f"Файл не найден: {file_path}"
        logger.error(error_msg)
        return []
    except json.JSONDecodeError as e:
        error_msg = f"Ошибка декодирования JSON в файле {file_path}: {str(e)}"
        logger.error(error_msg)
        return []
    except Exception as e:
        error_msg = f"Неизвестная ошибка при загрузке файла {file_path}: {str(e)}"
        logger.error(error_msg)
        return []
