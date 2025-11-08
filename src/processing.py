def filter_by_state(operations: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список операций по состоянию"""
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(operations: list[dict], reverse: bool = True) -> list[dict]:
    """Сортирует список операций по дате."""
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)