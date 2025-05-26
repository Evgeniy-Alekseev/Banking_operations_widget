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
