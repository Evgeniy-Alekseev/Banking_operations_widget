import json
import logging
from pathlib import Path
from typing import Dict, List

logging.basicConfig(
    filename="../logs/utils.log",
    encoding="utf-8",
    filemode="w",
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


def load_transactions_json(file_path: str = "operations.json") -> List[Dict]:
    """
    Загружает список транзакций из JSON-файла и возвращает список словарей
    с транзакциями или пустой список в случае ошибок
    """
    try:
        logger.info("Запуск приложения")
        if not Path(file_path).exists():
            return []

        logger.info("Запуск чтения данных из файла")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logger.info("Данные загружены успешно")
            if isinstance(data, list):
                return data
            return []
            logger.info("Данные для загрузки не найдены")
    except (json.JSONDecodeError, FileNotFoundError, PermissionError) as ex:
        # Обрабатываем ошибки:
        # - Невалидный JSON
        # - Файл не найден
        # - Нет прав на чтение
        logger.error(f"Ошибка {ex}")
        return []
        logger.info("Завершение работы приложения")


if __name__ == "__main__":
    load_transactions_json()
