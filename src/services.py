import re


from collections import Counter


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Фильтрует список транзакций, оставляя только те, в описании которых встречается заданная строка.

    Принимает список словарей с транзакциями (должен содержать ключ "description").
    Возвращает список словарей, у которых в поле "description" найдено совпадение с `search`.
    Если `search` пуст, возвращает пустой список.
    search: Строка для поиска в описании.
    """
    if not search:
        return []  #  Возвращает пустой список при пустом поиске

    pattern = re.compile(re.escape(search), re.IGNORECASE)  # Без учета регистра
    filtered_data = []

    for transaction in data:
        description = transaction.get("description", "")
        if pattern.search(description):
            filtered_data.append(transaction)

    return filtered_data


def process_bank_operations(data: list[dict], categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество операций для каждой категории из списка.
    Принимает список словарей с данными о банковских операциях и список категорий операций (должен содержать ключ "description").
    Возвращает словарь, где ключи — категории, а значения — количество операций.
    Если категория не встречается, её значение будет 0.
    """
    descriptions = [transaction.get("description", "").lower() for transaction in data]

    category_counts = Counter()

    for category in categories:
        lower_category = category.lower()
        category_counts[category] = sum(1 for desc in descriptions if lower_category in desc)

    return dict(category_counts)
