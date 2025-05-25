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