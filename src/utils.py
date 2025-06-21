import json
from pathlib import Path
from typing import Dict, List


def load_transactions(file_path: str = "operations.json") -> List[Dict]:
    """
    Загружает список транзакций из JSON-файла и возвращает список словарей
    с транзакциями или пустой список в случае ошибок
    """
    try:
        if not Path(file_path).exists():
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            return []

    except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
        # Обрабатываем ошибки:
        # - Невалидный JSON
        # - Файл не найден
        # - Нет прав на чтение
        return []
