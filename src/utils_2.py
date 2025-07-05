import csv
from pathlib import Path
from typing import Dict, List

import pandas as pd


def load_transactions_csv(file_path: str = "transactions.csv") -> List[Dict]:
    """
    Загружает список транзакций из CSV-файла и возвращает список словарей
    с транзакциями или пустой список в случае ошибок
    """
    try:
        if not Path(file_path).exists():
            return []

        with open("transactions.csv", "r", encoding="utf-8") as file:
            data_csv = list(csv.DictReader(file))
            return data_csv

    except (csv.Error, FileNotFoundError, PermissionError):
        # Обрабатываем ошибки:
        # - Невалидный CSV
        # - Файл не найден
        # - Нет прав на чтение
        return []


if __name__ == "__main__":
    load_transactions_csv()


def load_transactions_excel(file_path: str = "transactions_excel.xlsx") -> List[Dict]:
    """
    Загружает список транзакций из EXCEL-файла и возвращает список словарей
    с транзакциями или пустой список в случае ошибок
    """
    try:
        if not Path(file_path).exists():
            return []

        df = pd.read_excel("transactions_excel.xlsx")
        df_excel = df.to_dict("records")
        return df_excel

    except (FileNotFoundError, PermissionError, pd.errors.EmptyDataError, ValueError, KeyError, ImportError):
        # Обрабатываем ошибки:
        # - Невалидный EXCEL
        # - Файл не найден
        # - Нет прав на чтение
        # - Неверная структура массива данных
        # - Неверный импорт
        return []


if __name__ == "__main__":
    load_transactions_csv()
