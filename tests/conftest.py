import pytest


# фикстуры для get_mask_card_number

@pytest.fixture
def mask_card_number():
    return "1234 56** **** 3456"


@pytest.fixture
def different_input_card_number():
    return "1234 56** **** 3456"

@pytest.fixture
def invalid_length_card_number():
    return "Номер карты должен содержать 16 цифр"


@pytest.fixture
def non_digit_card_number():
    return "Номер карты должен содержать 16 цифр"


# фикстуры для get_mask_account

@pytest.fixture
def mask_account():
    return "**7890"


@pytest.fixture
def different_input_account():
    return "**7890"


@pytest.fixture
def min_length_account():
    return "**1234"


@pytest.fixture
def invalid_length_account():
    return "Номер счёта должен содержать минимум 4 цифры"


@pytest.fixture
def non_digit_account():
    return "Номер счёта должен содержать минимум 4 цифры"


# фикстуры для mask_account_card

@pytest.fixture
def widget_mask_card():
      return [
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("MasterCard 1111222233334444", "MasterCard 1111 22** **** 4444"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456")
        ]

@pytest.fixture(params=[
    ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
    ("MasterCard 1111222233334444", "MasterCard 1111 22** **** 4444"),
    ("МИР 1234567890123456", "МИР 1234 56** **** 3456")
])
def card_test_data(request):
    return request.param

# Фикстуры для теста маскировки счетов
@pytest.fixture(params=[
    ("Счет 12345678901234567890", "Счет **7890"),
    ("Счет 98765432109876543210", "Счет **3210")
])
def account_test_data(request):
    return request.param

# Фикстуры для теста некорректных данных
@pytest.fixture(params=[
    ("Visa Platinum 1234", "Номер карты должен содержать только цифры"),
    ("MasterCard abcdefghijklmnop", "Номер карты должен содержать только цифры"),
    ("Visa Platinum", "Номер карты должен содержать только цифры")
])
def invalid_card_data(request):
    return request.param

@pytest.fixture(params=[
    ("Счет 123", "Номер счета должен содержать минимум 4 цифры"),
    ("Счет abc", "Номер счета должен содержать только цифры")
])
def invalid_account_data(request):
    return request.param


# фикстуры для get_date

@pytest.fixture
def valid_dates():
    """Фикстура с валидными датами и ожидаемыми результатами"""
    return [
        ("2024-03-11T12:30:45", "11.03.2024"),
        ("1999-12-31T23:59:59", "31.12.1999"),
        ("2000-01-01T00:00:00", "01.01.2000"),
        ("2024-03-11", "11.03.2024"),
        ("2024-03-11 12:30:45", "11.03.2024"),
        ("0001-01-01T00:00:00", "01.01.0001"),
        ("2020-02-29T12:00:00", "29.02.2020"),
        ("2023-12-31T23:59:59", "31.12.2023")
    ]

@pytest.fixture
def invalid_dates():
    """Фикстура с невалидными форматами дат"""
    return [
        "",
        "2024/03/11",
        "11-03-2024",
        "T12:30:45",
        "invalid date string",
        "2024-03"
    ]
