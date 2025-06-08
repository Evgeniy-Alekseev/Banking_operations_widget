import pytest

from src.masks import get_mask_account, get_mask_card_number

# тесты для get_mask_card_number


def test_get_mask_card_number(mask_card_number):
    """Проверяет, что функция корректно маскирует номер карты в стандартном формате."""
    assert get_mask_card_number("1234567890123456") == mask_card_number
    assert get_mask_card_number("1234 5678 9012 3456") == mask_card_number


def test_different_input_formats(different_input_card_number):
    """
    Проверяет, что функция корректно обрабатывает разные форматы ввода (с пробелами,
    без пробелов, с другими разделителями).
    """
    assert get_mask_card_number("1234567890123456") == different_input_card_number
    assert get_mask_card_number("1234 5678 9012 3456") == different_input_card_number
    assert get_mask_card_number("1234-5678-9012-3456".replace("-", " ")) == different_input_card_number


def test_invalid_card_lengths(invalid_length_card_number):
    """Проверка обработки нестандартных длин номеров."""
    # Фикстура должна возвращать список кортежей (номер, сообщение)
    for card_number, expected_message in invalid_length_card_number:
        with pytest.raises(ValueError, match=expected_message):
            get_mask_card_number(card_number)


def test_non_digit_characters():
    """Проверяет обработку номеров с нецифровыми символами."""
    # Буквы вместо цифр
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number("1234abcd5678efgh")
    # Специальный символ
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number("1234 5678 9012 345!")
    # Смесь цифр и символов
    with pytest.raises(ValueError, match="Номер карты должен содержать только цифры"):
        get_mask_card_number("1234-5678-9012-3456")


# Использование параметризации для get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("1234 5678 9012 3456", "1234 56** **** 3456"),
        ("1234-5678-9012-3456".replace("-", " "), "1234 56** **** 3456"),
    ],
)
def test_valid_card_number(card_number, expected):
    """Проверяет, что функция корректно маскирует номер карты с ввода в различных форматах."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "card_number,expected_error",
    [
        ("1234567890", "Номер карты должен содержать 16 цифр"),  # 10 цифр
        ("12345678901234567890", "Номер карты должен содержать 16 цифр"),  # 20 цифр
        ("", "Номер карты не может быть пустым"),  # Пустая строка
        ("     ", "Номер карты не может быть пустым"),  # Только пробелы
    ],
)
def test_invalid_card_numbers(card_number, expected_error):
    """Параметризованный тест невалидных номеров карт"""
    with pytest.raises(ValueError, match=expected_error):
        get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "invalid_card_number, expected_message",
    [
        ("", "Номер карты не может быть пустым"),
        ("     ", "Номер карты не может быть пустым"),
        ("1234abcd5678efgh", "Номер карты должен содержать только цифры"),
        ("1234 5678 9012 345!", "Номер карты должен содержать только цифры"),
        ("1234567890", "Номер карты должен содержать 16 цифр"),
        ("12345678901234567890", "Номер карты должен содержать 16 цифр"),
    ],
)
def test_invalid_card_number(invalid_card_number, expected_message):
    """Проверяет обработку невалидных номеров карт."""
    with pytest.raises(ValueError, match=expected_message):
        get_mask_card_number(invalid_card_number)


# тесты для get_mask_account


def test_get_mask_account(mask_account):
    """Проверяет, что функция корректно маскирует номер карты в стандартном формате."""
    assert get_mask_account("12345678901234567890") == mask_account
    assert get_mask_account("12345 67890 12345 67890") == mask_account


def test_different_input_formats(different_input_account):
    """
    Проверяет, что функция корректно обрабатывает разные форматы ввода (с пробелами,
    без пробелов, с другими разделителями).
    """
    assert get_mask_account("12345678901234567890") == different_input_account
    assert get_mask_account("12345 67890 12345 67890") == different_input_account
    assert get_mask_account("12345-67890-12345-67890".replace("-", " ")) == different_input_account


def test_min_length(min_length_account):
    """Проверка работы функции с минимально допустимой длиной (4 символа)."""
    assert get_mask_account("1234") == min_length_account
    assert get_mask_account("12 34") == min_length_account


def test_invalid_length(invalid_length_account):
    for account_number, expected_message in invalid_length_account:
        with pytest.raises(ValueError, match=expected_message):
            get_mask_account(account_number)


def test_none_input():
    """Проверка обработки None в качестве ввода"""
    with pytest.raises(ValueError):
        get_mask_account(None)


def test_non_digit_characters(non_digit_account):
    """Проверяет, что функция вызывает исключение, если в номере счёта есть нецифровые символы."""
    for account_number, expected_message in non_digit_account:
        with pytest.raises(ValueError, match=expected_message):
            get_mask_account(account_number)


# Использование параметризации для get_mask_account


@pytest.mark.parametrize(
    "input_value, expected_error",
    [
        (None, "Номер счёта не может быть None"),
        ("", "Номер счёта не может быть пустым"),
        ("   ", "Номер счёта не может быть пустым"),
        ("abc", "Номер счёта должен содержать только цифры"),
        ("123", "Номер счёта должен содержать минимум 4 цифры"),
    ],
)
def test_invalid_accounts(input_value, expected_error):
    """Проверка обработки невалидных номеров счетов"""
    with pytest.raises(ValueError, match=expected_error):
        get_mask_account(input_value)


@pytest.mark.parametrize(
    "input_value, expected_result",
    [
        ("12345678", "**5678"),
        ("1234 5678", "**5678"),
        ("0000111122223333", "**3333"),
    ],
)
def test_valid_accounts(input_value, expected_result):
    """Проверка корректных номеров счетов"""
    assert get_mask_account(input_value) == expected_result
