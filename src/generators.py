
transactions = ([{"id": 939719570,"state": "EXECUTED", "date": "2018-06-30T02:08:58.425572",
                  "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации", "from": "Счет 75106830613657916952", "to": "Счет 11776614605963066702"},
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]
)

def filter_by_currency(transactions: list[dict], currency: str) -> iter:
    """
    Фильтрует транзакции по валюте и возвращает итератор.
    """
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


if __name__ == "__main__":
    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))


def transaction_descriptions(transactions: list[dict]) -> iter:
    """
    Генератор, который возвращает описания транзакций по запросу.
    """
    for transaction in transactions:
        if "description" in transaction:
            yield transaction["description"]


if __name__ == "__main__":
    descriptions = transaction_descriptions(transactions)
    for _ in range(5):
        print(next(descriptions))


def card_number_generator(start: int, stop: int) -> iter:
    """
    Генератор номеров банковских карт, генерирует номера от start до stop
    включительно, в формате XXXX XXXX XXXX XXXX.
    """
    for number in range(start, stop + 1):
        card_str = f"{number:016d}"
        card_number = " ".join([card_str[i:i + 4] for i in range(0, 16, 4)])
        yield card_number


if __name__ == "__main__":
    for card_number in card_number_generator(1, 5):
        print(card_number)