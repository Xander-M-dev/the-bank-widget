"""Модуль для чтения финансовых операций из различных форматов файлов."""

from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """Читает финансовые операции из CSV-файла."""
    try:
        # Проверяем существование файла
        if not Path(file_path).exists():
            return []

        # Читаем CSV файл с помощью pandas
        df = pd.read_csv(file_path)

        # Конвертируем DataFrame в список словарей
        transactions = df.to_dict("records")

        return transactions

    except Exception as e:
        print(f"Ошибка при чтении CSV файла {file_path}: {e}")
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """Читает финансовые операции из Excel-файла."""
    try:
        # Проверяем существование файла
        if not Path(file_path).exists():
            return []

        # Читаем Excel файл с помощью pandas
        df = pd.read_excel(file_path)

        # Конвертируем DataFrame в список словарей
        transactions = df.to_dict("records")

        return transactions

    except Exception as e:
        print(f"Ошибка при чтении Excel файла {file_path}: {e}")
        return []
