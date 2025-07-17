import os

import pytest

from src.generators import card_number_generator

# фикстуры для get_mask_card_number


@pytest.fixture
def mask_card_number():
    return "1234 56** **** 3456"


@pytest.fixture
def different_input_card_number():
    return "1234 56** **** 3456"


@pytest.fixture
def invalid_length_card_number():
    return [
        ("1234567890", "Номер карты должен содержать 16 цифр"),
        ("12345678901234567890", "Номер карты должен содержать 16 цифр"),
        ("", "Номер карты не может быть пустым"),
        ("     ", "Номер карты не может быть пустым"),
        ("1234abcd5678efgh", "Номер карты должен содержать только цифры"),
    ]


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
    return [
        ("123", "Номер счёта должен содержать минимум 4 цифры"),
        ("", "Номер счёта не может быть пустым"),
        ("   ", "Номер счёта не может быть пустым"),
    ]


@pytest.fixture
def non_digit_account():
    return [
        ("1234abcd5678efgh", "Номер счёта должен содержать только цифры"),
        ("123", "Номер счёта должен содержать минимум 4 цифры"),
    ]


# фикстуры для mask_account_card


@pytest.fixture
def widget_mask_card():
    return [
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("MasterCard 1111222233334444", "MasterCard 1111 22** **** 4444"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
    ]


@pytest.fixture(
    params=[
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("MasterCard 1111222233334444", "MasterCard 1111 22** **** 4444"),
        ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
    ]
)
def card_test_data(request):
    return request.param


# Фикстуры для теста маскировки счетов
@pytest.fixture(params=[("Счёт 12345678901234567890", "Счёт **7890"), ("Счёт 98765432109876543210", "Счёт **3210")])
def account_test_data(request):
    return request.param


# Фикстуры для теста некорректных данных
@pytest.fixture(
    params=[
        ("Visa Platinum 1234", "Номер карты должен содержать 16 цифр"),
        ("Visa Platinum abcdefghijklmnop", "Номер карты должен содержать только цифры"),
    ]
)
def invalid_card_data(request):
    return request.param


@pytest.fixture(
    params=[
        ("Счет 123", "Номер счёта должен содержать минимум 4 цифры"),
        ("Счет abc", "Номер счёта должен содержать только цифры"),
    ]
)
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
        ("2023-12-31T23:59:59", "31.12.2023"),
    ]


@pytest.fixture
def invalid_dates():
    """Фикстура с невалидными форматами дат"""
    return ["", "2024/03/11", "11-03-2024", "T12:30:45", "invalid date string", "2024-03"]


# фикстуры для filter_by_state


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED", "amount": "100"},
        {"id": 2, "state": "PENDING", "amount": "200"},
        {"id": 3, "state": "EXECUTED", "amount": "300"},
        {"id": 4, "state": "CANCELED", "amount": "400"},
        {"id": 5, "state": "EXECUTED", "amount": "500"},
    ]


@pytest.fixture
def empty_transactions():
    """Фикстура с пустым списком транзакций"""
    return []


@pytest.fixture
def no_executed_transactions():
    """Фикстура без EXECUTED транзакций"""
    return [
        {"id": 1, "state": "PENDING", "amount": "100"},
        {"id": 2, "state": "CANCELED", "amount": "200"},
    ]


# фикстуры для sort_by_date


@pytest.fixture
def transactions_with_different_dates():
    """Фикстура с транзакциями разных дат и статусов"""
    return [
        {"id": 1, "date": "2023-08-15T12:00:00", "state": "EXECUTED"},
        {"id": 2, "date": "2023-08-20T15:30:00", "state": "PENDING"},
        {"id": 3, "date": "2023-08-10T09:15:00", "state": "EXECUTED"},
        {"id": 4, "date": "2023-08-20T10:00:00", "state": "CANCELED"},
        {"id": 5, "date": "2023-08-25T18:45:00", "state": "EXECUTED"},
    ]


@pytest.fixture
def transactions_with_same_dates():
    """Фикстура с транзакциями одинаковых дат, но разных статусов"""
    return [
        {"id": 1, "date": "2023-08-15T12:00:00", "state": "EXECUTED"},
        {"id": 2, "date": "2023-08-15T12:00:00", "state": "PENDING"},
        {"id": 3, "date": "2023-08-15T12:00:00", "state": "CANCELED"},
    ]


@pytest.fixture
def mixed_transactions():
    """Фикстура со смешанными данными: валидные и невалидные даты, разные статусы"""
    return [
        {"id": 1, "date": "2023-08-15T12:00:00", "state": "EXECUTED"},
        {"id": 2, "date": "invalid-date", "state": "PENDING"},
        {"id": 3, "date": "2023-08-10T09:15:00", "state": "EXECUTED"},
        {"id": 4, "date": None, "state": "CANCELED"},
        {"id": 5, "state": "EXECUTED"},  # Нет ключа date
    ]


@pytest.fixture
def edge_case_transactions():
    """Фикстура с граничными случаями"""
    return [
        {"id": 1, "date": "0001-01-01T00:00:00", "state": "EXECUTED"},  # Минимальная дата
        {"id": 2, "date": "9999-12-31T23:59:59", "state": "PENDING"},  # Максимальная дата
        {"id": 3, "date": "2020-02-29T12:00:00", "state": "EXECUTED"},  # Високосный год
    ]


@pytest.fixture
def large_transactions_set():
    """Генерация большого набора данных для тестирования производительности"""
    return [{"id": i, "date": f"2023-08-{i % 30+1}T12:00:00", "state": "EXECUTED"} for i in range(1000)]


# фикстуры для filter_by_currency


@pytest.fixture
def transactions_fixture():
    """Фикстура с тестовыми данными транзакций"""
    return [
        {"id": 939719570, "state": "EXECUTED", "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 142264268, "state": "EXECUTED", "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 873106923, "state": "EXECUTED", "operationAmount": {"currency": {"code": "RUB"}}},
        {"id": 895315941, "state": "EXECUTED", "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 594226727, "state": "CANCELED", "operationAmount": {"currency": {"code": "RUB"}}},
    ]


# фикстуры для transaction_descriptions


@pytest.fixture
def transactions_descriptions_fixture():
    """Фикстура с полными тестовыми данными транзакций"""
    return [
        {
            "id": 939719570,
            "description": "Перевод организации",
            "operationAmount": {"currency": {"code": "USD"}},
            "state": "EXECUTED",
        },
        {
            "id": 142264268,
            "description": "Перевод со счета на счет",
            "operationAmount": {"currency": {"code": "USD"}},
            "state": "EXECUTED",
        },
        {
            "id": 873106923,
            "description": "Перевод со счета на счет",
            "operationAmount": {"currency": {"code": "RUB"}},
            "state": "EXECUTED",
        },
        {
            "id": 895315941,
            "description": "Перевод с карты на карту",
            "operationAmount": {"currency": {"code": "USD"}},
            "state": "EXECUTED",
        },
        {
            "id": 594226727,
            "description": "Перевод организации",
            "operationAmount": {"currency": {"code": "RUB"}},
            "state": "CANCELED",
        },
    ]


@pytest.fixture
def empty_transactions_fixture():
    """Фикстура с пустым списком транзакций"""
    return []


@pytest.fixture
def no_description_transactions_fixture():
    """Фикстура с транзакциями без описания"""
    return [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "description": None, "operationAmount": {"currency": {"code": "RUB"}}},
        {"id": 3, "operationAmount": {"currency": {"code": "EUR"}}},
    ]


# фикстуры для card_number_generator


@pytest.fixture
def card_number_generator_fixture():
    """Фикстура для генератора номеров карт"""

    def _generator(start, stop):
        return card_number_generator(start, stop)

    return _generator


# Фикстура для декоратора log
@pytest.fixture
def log_file(tmp_path):
    filename = tmp_path / "test_log.txt"
    yield filename
    if os.path.exists(filename):
        os.remove(filename)


# фикстуры для load_transactions


@pytest.fixture
def sample_data():
    return [{"id": 1, "amount": "100", "currency": "RUB"}, {"id": 2, "amount": "200", "currency": "USD"}]


# фикстуры для get_amount_in_rub


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {"rates": {"RUB": 75.50}}
    mock.raise_for_status.return_value = None
    return mock


# фикстуры для process_bank_search


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "amount": 100, "description": "Payment for groceries"},
        {"id": 2, "amount": 200, "description": "Salary"},
        {"id": 3, "amount": 50, "description": "Cafe payment"},
        {"id": 4, "amount": 300, "description": "Monthly rent"},
        {"id": 5, "amount": 150, "description": "Tax (2023)"},
        {"id": 6, "amount": 75, "description": ""},  # Пустое описание
        {"id": 7, "amount": 90},  # Нет ключа 'description'
    ]


# фикстуры для process_bank_operations


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "description": "Salary ACME Corp"},
        {"id": 2, "description": "Grocery Store"},
        {"id": 3, "description": "Tax payment 2023"},
        {"id": 4, "description": "Bonus"},
        {"id": 5, "description": "Monthly salary"},
    ]
