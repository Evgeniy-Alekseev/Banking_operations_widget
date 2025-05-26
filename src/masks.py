from typing import Union


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты в виде числа и возвращает маску номера по правилу XXXX XX** **** XXXX"""
    cleaned_number = card_number.replace(" ", "")
    if not cleaned_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    if len(cleaned_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")
    return f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"


if __name__ == '__main__':
    print(get_mask_card_number("7000792289606361"))  # Вывод: "7000 79** **** 6361"


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета в виде числа и возвращает маску номера по правилу **XXXX"""
    cleaned_number = account_number.replace(" ", "")

    if not cleaned_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")
    if len(cleaned_number) < 4:
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    return f"**{cleaned_number[-4:]}"


if __name__ == '__main__':
    print(get_mask_account("73654108430135874305"))  # Вывод: "**4305"
