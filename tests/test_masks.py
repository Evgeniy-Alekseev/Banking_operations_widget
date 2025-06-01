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


def test_invalid_length(invalid_length_card_number):
    """Проверка обработки нестандартных длин номеров, только пробелов или пустую строку."""
    with pytest.raises(ValueError, match=invalid_length_card_number):
        get_mask_card_number("1234567890")  # Меньше 16 символов
    with pytest.raises(ValueError, match=invalid_length_card_number):
        get_mask_card_number("12345678901234567890")  # Больше 16 символов
    with pytest.raises(ValueError, match=invalid_length_card_number):
        get_mask_card_number("")  # Пустая строка
    with pytest.raises(ValueError, match=invalid_length_card_number):
        get_mask_card_number("     ")  # Только пробелы


def test_non_digit_characters(non_digit_card_number):
    """Проверяет, что функция вызывает исключение, если в номере карты есть нецифровые символы."""
    with pytest.raises(ValueError, match=non_digit_card_number):
        get_mask_card_number("1234abcd5678efgh")  # Буквы вместо цифр
    with pytest.raises(ValueError, match=non_digit_card_number):
        get_mask_card_number("1234 5678 9012 345!")  # Специальный символ


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
    "invalid_card_number, expected",
    [
        ("1234567890", ValueError),
        ("12345678901234567890", ValueError),
        ("1234abcd5678efgh", ValueError),
        ("1234 5678 9012 345!", ValueError),
        ("", ValueError),
        ("     ", ValueError),
    ],
)
def test_invalid_card_number(invalid_card_number, expected):
    """Проверяет, что функция корректно обрабатывает случаи неверного ввода и выдает исключения."""
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
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
    """Проверка обработки нестандартных длин номеров, только пробелов или пустую строку."""
    # Проверка короткого номера (менее 4 цифр)
    with pytest.raises(ValueError, match="Номер счёта должен содержать минимум 4 цифры"):
        get_mask_account("123")

    # Проверка пустой строки и пробелов
    with pytest.raises(ValueError, match="Номер счёта должен содержать только цифры"):
        get_mask_account("")
        get_mask_account("   ")


def test_non_digit_characters(non_digit_account):
    """Проверяет, что функция вызывает исключение, если в номере карты есть нецифровые символы."""
    with pytest.raises(ValueError, match=non_digit_account):
        get_mask_account("1234abcd5678efgh")  # Буквы вместо цифр
    with pytest.raises(ValueError, match=non_digit_account):
        get_mask_account("1234 5678 9012 345!")  # Специальный символ


def test_none_input():
    """Проверка обработки None в качестве ввода"""
    with pytest.raises(AttributeError):
        get_mask_account(None)





# Использование параметризации для get_mask_account


@pytest.mark.parametrize("input_value, expected_error", [
    (None, "Номер счёта не может быть None"),
    ("", "Номер счёта не может быть пустым"),
    ("   ", "Номер счёта не может быть пустым"),
    ("abc", "Номер счёта должен содержать только цифры"),
    ("123", "Номер счёта должен содержать минимум 4 цифры"),
    ("12 34", "Номер счёта должен содержать минимум 4 цифры"),
])
def test_invalid_accounts(input_value, expected_error):
    """Проверка обработки невалидных номеров счетов"""
    with pytest.raises(ValueError, match=expected_error):
        get_mask_account(input_value)

@pytest.mark.parametrize("input_value, expected_result", [
    ("12345678", "**5678"),
    ("1234 5678", "**5678"),
    ("0000111122223333", "**3333"),
])
def test_valid_accounts(input_value, expected_result):
    """Проверка корректных номеров счетов"""
    assert get_mask_account(input_value) == expected_result
