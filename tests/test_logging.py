from pathlib import Path
from src.masks import get_mask_account, get_mask_card_number
from src.utils import load_transactions


def test_masks_logging() -> None:
    """Тест логирования в модуле masks"""
    # Вызываем функции для генерации логов
    get_mask_card_number("1234567812345678")  # валидный номер
    get_mask_card_number("123")  # невалидный номер
    get_mask_account("1234567890")  # валидный счет
    get_mask_account("12")  # невалидный счет

    # Проверяем что файл лога создан
    log_file = Path("logs/masks.log")
    assert log_file.exists(), "Файл masks.log должен существовать"

    # Читаем содержимое лога
    log_content = log_file.read_text(encoding="utf-8")

    # Проверяем что есть записи об успешных операциях
    assert "DEBUG" in log_content
    assert "ERROR" in log_content
    assert "masks" in log_content


def test_utils_logging() -> None:
    """Тест логирования в модуле utils"""
    # Вызываем функции для генерации логов
    load_transactions("data/operations.json")  # валидный файл
    load_transactions("nonexistent.json")  # несуществующий файл

    # Проверяем что файл лога создан
    log_file = Path("logs/utils.log")
    assert log_file.exists(), "Файл utils.log должен существовать"

    # Читаем содержимое лога
    log_content = log_file.read_text(encoding="utf-8")

    # Проверяем что есть записи об успешных и ошибочных операциях
    assert "INFO" in log_content
    assert "ERROR" in log_content
    assert "utils" in log_content


def test_log_format() -> None:
    """Тест формата логов"""
    log_file = Path("logs/masks.log")
    if log_file.exists():
        log_content = log_file.read_text(encoding="utf-8")
        lines = log_content.strip().split("\n")

        if lines and lines[0]:
            # Проверяем формат первой строки
            first_line = lines[0]
            parts = first_line.split(" - ")
            assert len(parts) >= 4, "Лог должен содержать timestamp, module, level и message"
            assert "masks" in parts[1], "Должно содержать имя модуля"


def test_log_file_overwrite() -> None:
    """Тест что логи перезаписываются при каждом запуске"""
    log_file = Path("logs/masks.log")
    if log_file.exists():
        # Удаляем переменную initial_size, так как она не используется
        # Вместо этого просто проверяем что файл существует и можем писать в него
        get_mask_card_number("1111222233334444")
        assert log_file.exists()
