def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Функция возвращает список словарей,содержащий только те,у которых ключ соответствует указанному значению"""
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """Функция должна возвращать новый список, отсортированный по дате"""
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)
