import pytest
import os
import tempfile
from src.decorators import log


def test_log_decorator_success_console(capsys):
    """Тест декоратора log при успешном выполнении (вывод в консоль)"""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(2, 3)

    assert result == 5

    captured = capsys.readouterr()
    assert "add ok" in captured.out


def test_log_decorator_error_console(capsys):
    """Тест декоратора log при ошибке (вывод в консоль)"""

    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error" in captured.out
    assert "ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0)" in captured.out


def test_log_decorator_success_file():
    """Тест декоратора log при успешном выполнении (запись в файл)"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_filename = f.name

    try:
        @log(filename=temp_filename)
        def multiply(a: int, b: int) -> int:
            return a * b

        result = multiply(4, 5)

        assert result == 20

        with open(temp_filename, 'r', encoding='utf-8') as f:
            log_content = f.read()

        assert "multiply ok" in log_content

    finally:
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_log_decorator_error_file():
    """Тест декоратора log при ошибке (запись в файл)"""

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        temp_filename = f.name

    try:
        @log(filename=temp_filename)
        def failing_function(x: int) -> int:
            raise ValueError("Test error")

        with pytest.raises(ValueError):
            failing_function(42)

        with open(temp_filename, 'r', encoding='utf-8') as f:
            log_content = f.read()

        assert "failing_function error" in log_content
        assert "ValueError" in log_content
        assert "Inputs: (42,)" in log_content

    finally:
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)


def test_log_decorator_preserves_function_metadata():
    """Тест, что декоратор сохраняет метаданные функции"""

    @log()
    def test_func(a: int, b: int) -> int:
        """Тестовая функция"""
        return a + b

    assert test_func.__name__ == "test_func"
    assert test_func.__doc__ == "Тестовая функция"


def test_log_decorator_with_keyword_arguments(capsys):
    """Тест декоратора log с именованными аргументами"""

    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")

    assert result == "Hi, Alice!"

    captured = capsys.readouterr()
    assert "greet ok" in captured.out


def test_log_decorator_with_no_arguments(capsys):
    """Тест декоратора log с функцией без аргументов"""

    @log()
    def get_answer() -> int:
        return 42

    result = get_answer()

    assert result == 42

    captured = capsys.readouterr()
    assert "get_answer ok" in captured.out
