import json
import logging
import os
from pathlib import Path
from typing import Dict, List


logging.basicConfig(
    filename='../logs/utils.log',
    encoding="utf-8",
    filemode='w',
    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def load_transactions(file_path: str = "operations.json") -> List[Dict]:
    """
    Загружает список транзакций из JSON-файла и возвращает список словарей
    с транзакциями или пустой список в случае ошибок
    """
    try:
        logger.info('Запуск приложения')
        if not Path(file_path).exists():
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if isinstance(data, list):
                return data
            return []

    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        # Обрабатываем ошибки:
        # - Невалидный JSON
        # - Файл не найден
        # - Нет прав на чтение
        return []


if __name__ == "__main__":
    load_transactions()
