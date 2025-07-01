import logging

logging.basicConfig(
    filename="../logs/masks.log",
    encoding="utf-8",
    filemode="w",
    format="%(asctime)s %(name)s %(levelname)s: %(message)s",
    level=logging.DEBUG,
)

card_num_logger = logging.getLogger("add.card_num")
account_logger = logging.getLogger("add.account")


def get_mask_card_number(card_number: str) -> str:
    """
    Функция принимает на вход номер карты в виде числа и возвращает маску номера по правилу XXXX XX** **** XXXX
    """
    card_num_logger.info("Запуск приложения")
    cleaned_number = card_number.replace(" ", "")

    # Проверка на пустую строку или строку из пробелов
    card_num_logger.info("Проверка введённых данных")
    if not cleaned_number:
        raise ValueError("Номер карты не может быть пустым")
        card_num_logger.error("Ошибка ввода данных")
    # Проверка на наличие только цифр
    if not cleaned_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
        card_num_logger.error("Ошибка ввода данных")

    # Проверка длины номера карты
    if len(cleaned_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
        card_num_logger.error("Ошибка ввода данных")

    # Собираем замаскированный номер
    card_num_logger.info("Номер замаскирован успешно")
    return f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"
    card_num_logger.info("Завершение работы приложения")


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))  # Вывод: "7000 79** **** 6361"


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает маску номера по правилу **XXXX"""

    account_logger.info("Запуск приложения")
    account_logger.info("Проверка введённых данных")
    if account_number is None:
        raise ValueError("Номер счёта не может быть None")
        account_logger.error("Ошибка ввода данных")

    if not isinstance(account_number, str):
        raise ValueError("Номер счёта должен быть строкой")
        account_logger.error("Ошибка ввода данных")

    cleaned_number = account_number.replace(" ", "")

    if not cleaned_number:
        raise ValueError("Номер счёта не может быть пустым")
        account_logger.error("Ошибка ввода данных")

    if not cleaned_number.isdigit():
        raise ValueError("Номер счёта должен содержать только цифры")
        account_logger.error("Ошибка ввода данных")

    if len(cleaned_number) < 4:
        raise ValueError("Номер счёта должен содержать минимум 4 цифры")
        account_logger.error("Ошибка ввода данных")

    account_logger.info("Номер замаскирован успешно")
    return f"**{cleaned_number[-4:]}"
    account_logger.info("Завершение работы приложения")


if __name__ == "__main__":
    print(get_mask_account("73654108430135874305"))  # Вывод: "**4305"
