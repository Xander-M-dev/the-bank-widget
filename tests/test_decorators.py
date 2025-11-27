import os
import tempfile

import pytest

from src.decorators import log


def test_log_decorator_success_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест декоратора log при успешном выполнении (вывод в консоль)"""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)

    # Проверяем результат функции
    assert result == 5

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_decorator_error_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест декоратора log при ошибке (вывод в консоль)"""

    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    # Проверяем, что исключение пробрасывается
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "divide error" in captured.out
    assert "ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0)" in captured.out


def test_log_decorator_success_file() -> None:
    """Тест декоратора log при успешном выполнении (запись в файл)"""

    # Создаем временный файл с помощью tempfile.mktemp чтобы избежать проблем с типами
    temp_filename = tempfile.mktemp(suffix=".txt")

    try:

        @log(filename=temp_filename)
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply(4, 5)

        # Проверяем результат функции
        assert result == 20

        # Проверяем запись в файл
        with open(temp_filename, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "multiply ok" in log_content

    finally:
        # Удаляем временный файл
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_log_decorator_error_file() -> None:
    """Тест декоратора log при ошибке (запись в файл)"""

    # Создаем временный файл с помощью tempfile.mktemp
    temp_filename = tempfile.mktemp(suffix=".txt")

    try:

        @log(filename=temp_filename)
        def failing_function(x: int) -> int:
            raise ValueError("Test error")

        # Проверяем, что исключение пробрасывается
        with pytest.raises(ValueError):
            failing_function(42)

        # Проверяем запись в файл
        with open(temp_filename, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "failing_function error" in log_content
        assert "ValueError" in log_content
        assert "Inputs: (42,)" in log_content

    finally:
        # Удаляем временный файл
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_log_decorator_preserves_function_metadata() -> None:
    """Тест, что декоратор сохраняет метаданные функции"""

    @log()
    def test_func(a: int, b: int) -> int:
        """Тестовая функция"""
        return a + b

    # Проверяем, что метаданные сохранились
    assert test_func.__name__ == "test_func"
    assert test_func.__doc__ == "Тестовая функция"


def test_log_decorator_with_keyword_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест декоратора log с именованными аргументами"""

    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")

    # Проверяем результат функции
    assert result == "Hi, Alice!"

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "greet ok" in captured.out


def test_log_decorator_with_no_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    """Тест декоратора log с функцией без аргументов"""

    @log()
    def get_answer() -> int:
        return 42

    result = get_answer()

    # Проверяем результат функции
    assert result == 42

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    assert "get_answer ok" in captured.out
