from datetime import datetime


def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Фильтрует список словарей по значению ключа 'state' (по умолчанию 'EXECUTED').
    Возвращает отфильтрованный список словарей.
    """
    return [transaction for transaction in transactions if transaction.get("state", None) == state.upper()]


if __name__ == "__main__":
    transactions = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    print(filter_by_state(transactions))


def sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]:
    """
    Сортирует список словарей по дате (ключ 'date') (по умолчанию reverse = True).
    Возвращает отсортированный список словарей (в начале новые записи).
    """
    for transaction in transactions:
        if "date" not in transaction:
            raise KeyError("Transaction is missing 'date' key")
        if transaction["date"] is None:
            raise ValueError("Transaction date is None")
        try:
            datetime.fromisoformat(transaction["date"])
        except ValueError as e:
            raise ValueError(f"Invalid date format: {transaction['date']}") from e

    return sorted(transactions, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)


if __name__ == "__main__":
    print(sort_by_date(transactions))
