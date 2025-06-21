import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def get_amount_in_rub(transaction: Dict) -> float:
    """
    Возвращает сумму транзакции в рублях.
    Если валюта не RUB, конвертирует по текущему курсу через API.
    """
    if not transaction or "operationAmount" not in transaction:
        return 0.0

    try:
        amount_data = transaction["operationAmount"]
        amount = float(amount_data["amount"])
        currency = amount_data["currency"]["code"].upper()

        if currency == "RUB":
            return amount

        # Получаем курс валюты к RUB
        response = requests.get(
            "https://api.apilayer.com/exchangerates_data/latest",
            params={"base": currency, "symbols": "RUB"},
            headers={"apikey": API_KEY},
            timeout=10,
        )
        response.raise_for_status()
        rate = response.json()["rates"]["RUB"]
        return round(amount * rate, 2)

    except (ValueError, KeyError, TypeError):
        return 0.0
    except requests.exceptions.RequestException:
        return 0.0
