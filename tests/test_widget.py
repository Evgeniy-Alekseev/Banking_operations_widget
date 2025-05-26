import pytest
from src.widget import mask_account_card



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