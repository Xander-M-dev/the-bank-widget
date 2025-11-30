import datetime
from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования выполнения функций."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__

            try:
                result = func(*args, **kwargs)

                log_message = f"{current_time} {func_name} ok\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")

                return result

            except Exception as e:
                error_message = f"{current_time} {func_name} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    print(error_message, end="")

                raise

        return wrapper

    return decorator
