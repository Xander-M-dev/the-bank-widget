import json
import os
import tempfile
from typing import Any, Dict, List

from src.utils import load_transactions


def test_load_transactions_valid_file() -> None:
    """Тест загрузки корректного JSON-файла"""
    # Создаем временный файл с корректными данными
    test_data: List[Dict[str, Any]] = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_data, f)
        temp_filename = f.name

    try:
        result = load_transactions(temp_filename)
        assert result == test_data
    finally:
        os.unlink(temp_filename)


def test_load_transactions_file_not_found() -> None:
    """Тест загрузки несуществующего файла"""
    result = load_transactions("nonexistent_file.json")
    assert result == []


def test_load_transactions_invalid_json() -> None:
    """Тест загрузки файла с невалидным JSON"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("invalid json content")
        temp_filename = f.name

    try:
        result = load_transactions(temp_filename)
        assert result == []
    finally:
        os.unlink(temp_filename)


def test_load_transactions_not_list() -> None:
    """Тест загрузки JSON, который не является списком"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"id": 1, "amount": 100}, f)  # объект, а не список
        temp_filename = f.name

    try:
        result = load_transactions(temp_filename)
        assert result == []
    finally:
        os.unlink(temp_filename)


def test_load_transactions_empty_file() -> None:
    """Тест загрузки пустого файла"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        pass  # пустой файл
        temp_filename = f.name

    try:
        result = load_transactions(temp_filename)
        assert result == []
    finally:
        os.unlink(temp_filename)
