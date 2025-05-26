import pytest
from datetime import datetime
from src.widget import mask_account_card, get_date



# тесты для mask_account_card

def test_mask_card(card_test_data):
    """Проверяет, что функция корректно маскирует номера карт разных платежных систем."""
    input_data, expected = card_test_data
    assert mask_account_card(input_data) == expected


def test_mask_account(account_test_data):
    """Проверяет, что функция корректно маскирует номера счетов."""
    input_data, expected = account_test_data
    assert mask_account_card(input_data) == expected


def test_empty_input():
    """Проверяет, что функция корректно обрабатывает пустую строку."""
    assert mask_account_card("") == ""


def test_invalid_card_number(invalid_card_data):
    """Проверяет, что функция вызывает исключение при некорректном номере карты."""
    input_data, error_message = invalid_card_data
    with pytest.raises(ValueError, match=error_message):
        mask_account_card(input_data)


def test_invalid_account_number(invalid_account_data):
    """Проверяет, что функция вызывает исключение при некорректном номере счета."""
    input_data, error_message = invalid_account_data
    with pytest.raises(ValueError, match=error_message):
        mask_account_card(input_data)


def test_unknown_format():
    """Проверяет, что функция возвращает исходную строку, если формат не соответствует ни карте, ни счету."""
    assert mask_account_card("Неизвестный формат 1234567890") == "Неизвестный формат 1234567890"


# Использование параметризации

@pytest.mark.parametrize("account, expected", [
    ("Счет 12345678901234567890", "Счет **7890"),
    ("Счет 98765432109876543210", "Счет **3210"),
    ("Счет 00000000000000000000", "Счет **0000"),
])
def test_mask_account_valid_accounts(account, expected):
    """Тестирование маскировки счетов с параметризацией."""
    assert mask_account_card(account) == expected


@pytest.mark.parametrize("card, expected", [
    ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
    ("Maestro 9876543210987654", "Maestro 9876 54** **** 7654"),
    ("МИР 0000000000000000", "МИР 0000 00** **** 0000"),
    ("MasterCard 5555555555554444", "MasterCard 5555 55** **** 4444"),
])
def test_mask_account_valid_cards(card, expected):
    """Тестирование маскировки карт с параметризацией."""
    assert mask_account_card(card) == expected

@pytest.mark.parametrize("invalid_input", [
    "",
    "Неизвестный формат 12345",
    "Счет",
    "Карта",
])
def test_mask_account_invalid_strings(invalid_input):
    """Тестирование обработки некорректных строковых входных данных."""
    result = mask_account_card(invalid_input)
    assert result == invalid_input

@pytest.mark.parametrize("input_data, expected", [
    ("  Счет  12345678901234567890  ", "Счет **7890"),
    ("  Visa Platinum  1234567890123456  ", "Visa Platinum 1234 56** **** 3456"),
])
def test_mask_account_with_whitespace(input_data, expected):
    """Тестирование обработки строк с лишними пробелами."""
    assert mask_account_card(input_data) == expected

# тесты для get_date

def test_different_date_formats(valid_dates):
    """Проверка работы с различными форматами даты"""
    # Проверяем разные форматы (индексы 3, 0, 4 из valid_dates)
    assert get_date(valid_dates[3][0]) == valid_dates[3][1]  # Дата без времени
    assert get_date(valid_dates[0][0]) == valid_dates[0][1]  # Дата с 'T'
    assert get_date(valid_dates[4][0]) == valid_dates[4][1]  # Дата с пробелом

    # Проверка пустой строки
    with pytest.raises(ValueError, match="Пустая строка не допускается."):
        get_date("")

    # Проверка некорректного формата
    with pytest.raises(ValueError):
        get_date("2024/03/11")


def test_edge_cases(valid_dates):
    """Проверка граничных случаев"""
    # Проверяем граничные случаи (индексы 5, 6, 7 из valid_dates)
    assert get_date(valid_dates[5][0]) == valid_dates[5][1]  # Минимальная дата
    assert get_date(valid_dates[6][0]) == valid_dates[6][1]  # 29 февраля
    assert get_date(valid_dates[7][0]) == valid_dates[7][1]  # 31 декабря


def test_invalid_input(invalid_dates):
    """Проверка обработки некорректных входных данных"""
    for date_str in invalid_dates:
        with pytest.raises(ValueError):
            get_date(date_str)


# Использование параметризации

@pytest.mark.parametrize("date_str, expected", [
    ("2024-03-11T12:30:45", "11.03.2024"),
    ("1999-12-31T23:59:59", "31.12.1999"),
    ("2000-01-01T00:00:00", "01.01.2000")
])
def test_correct_date_conversion(date_str, expected):
    """Тестирование правильности преобразования даты"""
    assert get_date(date_str) == expected

# Проверка работы с различными форматами даты
@pytest.mark.parametrize("date_str, expected", [
    ("2024-03-11", "11.03.2024"),
    ("2024-03-11T12:30:45", "11.03.2024"),
    ("2024-03-11 12:30:45", "11.03.2024")
])
def test_valid_date_formats(date_str, expected):
    """Проверка валидных форматов даты"""
    assert get_date(date_str) == expected

# Проверка граничных случаев
@pytest.mark.parametrize("date_str, expected", [
    ("0001-01-01T00:00:00", "01.01.0001"),
    ("2020-02-29T12:00:00", "29.02.2020"),
    ("2023-12-31T23:59:59", "31.12.2023")
])
def test_edge_cases(date_str, expected):
    """Проверка граничных случаев"""
    assert get_date(date_str) == expected

# Проверка обработки некорректных входных данных
@pytest.mark.parametrize("invalid_date", [
    "",
    "2024/03/11",
    "11-03-2024",
    "T12:30:45",
    "invalid date string",
    "2024-03"
])
def test_invalid_input(invalid_date):
    """Проверка обработки некорректных входных данных"""
    with pytest.raises(ValueError):
        get_date(invalid_date)