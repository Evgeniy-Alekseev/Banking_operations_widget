from typing import Dict, List, Any

from src.processing import filter_by_state, sort_by_date
from src.services import process_bank_operations, process_bank_search
from src.utils import load_transactions_json
from src.utils_2 import load_transactions_csv, load_transactions_excel


def get_user_input(prompt: str, valid_options: List[str] = None) -> str:
    """Получает ввод пользователя с проверкой"""
    while True:
        user_input = input(prompt).strip()
        if not valid_options or user_input.lower() in [v.lower() for v in valid_options]:
            return user_input
        print(f"Неверный ввод. Допустимые варианты: {', '.join(valid_options)}\n")


def get_user_choice(prompt: str, options: List[str]) -> str:
    """Получает выбор пользователя с проверкой"""
    while True:
        print(prompt)
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        choice = input("Ваш выбор: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("\nНеверный ввод. Пожалуйста, выберите один из предложенных вариантов.\n")


def print_transaction(transaction: Dict) -> None:
    """Печатает информацию о транзакции в заданном формате"""
    if not isinstance(transaction, dict):
        print("Ошибка: неверный формат транзакции")
        return

    date = transaction.get("date", "Нет даты")
    description = transaction.get("description", "Нет описания")
    print(f"{date} {description}")

    if "from" in transaction:
        print(f"{transaction['from']}", end="")
        if "to" in transaction:
            print(f" -> {transaction['to']}")
        else:
            print()
    elif "to" in transaction:
        print(f"{transaction['to']}")

    amount = transaction.get("amount", "")
    currency = transaction.get("currency", "")
    if currency and currency.upper() == "RUB":
        print(f"Сумма: {amount} руб.\n")
    else:
        print(f"Сумма: {amount} {currency}\n")


def main() -> None:
    """
    Объединяет функционал модулей для работы с трансакциями
    """
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбор типа файла
    file_type = get_user_choice("Выберите необходимый пункт меню:", ["JSON-файл", "CSV-файл", "XLSX-файл"])

    print(f"\nДля обработки выбран {file_type}.")

    # Загрузка данных
    try:
        if file_type == "JSON-файл":
            transactions = load_transactions_json("data/operations.json")
        elif file_type == "CSV-файл":
            transactions = load_transactions_csv("data/transactions.csv")
        else:
            transactions = load_transactions_excel("data/transactions_excel.xlsx")

        # Проверяем, что данные загружены правильно
        if not transactions or not all(isinstance(t, dict) for t in transactions):
            print("Ошибка: загруженные данные имеют неверный формат")
            return

    except Exception as e:
        print(f"\nОшибка при загрузке файла: {e}")
        return

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = (
            input(
                "\nВведите статус, по которому необходимо выполнить фильтрацию.\n"
                f"Доступные для фильтрации статусы: {', '.join(valid_statuses)}\n"
                "Ваш выбор: "
            )
            .strip()
            .upper()
        )

        if status in valid_statuses:
            break
        print(f'\nСтатус операции "{status}" недоступен.')

    filtered = filter_by_state(transactions, status)
    print(f'\nОперации отфильтрованы по статусу "{status}"')

    # Сортировка по дате
    sort_choice = get_user_input("\nОтсортировать операции по дате? (Да/Нет): ", ["Да", "Нет"]).lower()

    if sort_choice == "да":
        sort_order = get_user_input(
            "Отсортировать по возрастанию или по убыванию? (по возрастанию/по убыванию): ",
            ["по возрастанию", "по убыванию"],
        )
        reverse = sort_order == "по убыванию"
        filtered = sort_by_date(filtered, reverse)

    # Фильтрация рублевых транзакций
    rub_only = get_user_input("\nВыводить только рублевые транзакции? (Да/Нет): ", ["Да", "Нет"]).lower()

    if rub_only == "да":
        filtered = process_bank_operations(filtered, ["RUB"])

    # Поиск по описанию
    search_choice = get_user_input(
        "\nОтфильтровать список транзакций по определенному слову в описании? (Да/Нет): ", ["Да", "Нет"]
    ).lower()

    if search_choice == "да":
        search_word = input("Введите слово для поиска в описании: ").strip()
        filtered = process_bank_search(filtered, search_word)

    # Вывод результатов
    print("\nРаспечатываю итоговый список транзакций...\n")

    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(filtered)}\n")
    for transaction in filtered:
        if isinstance(transaction, dict):  # Дополнительная проверка
            print_transaction(transaction)
        else:
            print(f"Ошибка: неверный формат транзакции: {transaction}")


if __name__ == "__main__":
    main()
