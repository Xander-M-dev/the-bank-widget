"""Конфигурация логирования для проекта The Bank Widget."""

import logging
from pathlib import Path


def setup_logging(module_name: str) -> logging.Logger:
    """Настраивает и возвращает логгер для указанного модуля."""
    # Создаем папку logs если ее нет
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Логгер с именем модуля
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # Уровень DEBUG

    logger.handlers.clear()

    # Файловый обработчик
    log_file = logs_dir / f"{module_name}.log"
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")  # mode='w' для перезаписи
    file_handler.setLevel(logging.DEBUG)

    # Форматтер
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    # Обработчик логгера
    logger.addHandler(file_handler)

    return logger
