import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).parent.parent))
from src.processing import filter_by_state, sort_by_date

# тесты для filter_by_state


def test_filter_by_state(sample_transactions, state, expected_ids):
    """Тестирование фильтрации по разным статусам"""
    result = filter_by_state(sample_transactions, state)
    assert [t["id"] for t in result] == expected_ids


def test_empty_input(empty_transactions):
    """Проверка работы с пустым списком транзакций"""
    result = filter_by_state(empty_transactions)
    assert result == []


def test_no_matching_state(no_executed_transactions):
    """Проверка случая, когда нет транзакций с искомым статусом"""
    result = filter_by_state(no_executed_transactions)
    assert result == []


def test_default_state(sample_transactions):
    """Проверка работы функции со значением по умолчанию"""
    result = filter_by_state(sample_transactions)
    assert [t["id"] for t in result] == [1, 3, 5]


def test_missing_state_key(sample_transactions):
    """Проверка обработки транзакций без ключа 'state'"""
    # Добавляем транзакцию без ключа state
    sample_transactions.append({"id": 6, "amount": "600"})
    result = filter_by_state(sample_transactions, "EXECUTED")
    assert [t["id"] for t in result] == [1, 3, 5]


# Использование параметризации


@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("PENDING", [2]),
        ("CANCELED", [4]),
        ("UNKNOWN", []),
    ],
)
def test_filter_by_state(sample_transactions, state, expected_ids):
    """Параметризованный тест фильтрации по разным статусам"""
    result = filter_by_state(sample_transactions, state)
    assert [t["id"] for t in result] == expected_ids


# тесты для sort_by_date


def test_empty_list():
    """Проверка работы с пустым списком"""
    assert sort_by_date([]) == []


def test_single_transaction():
    """Проверка работы с одним элементом"""
    transaction = [{"id": 1, "date": "2023-08-15T12:00:00"}]
    assert sort_by_date(transaction) == transaction


# Использование параметризации


@pytest.mark.parametrize(
    "reverse, expected_order",
    [
        (True, [2, 4, 1, 3]),  # Сортировка по убыванию (новые сначала)
        (False, [3, 1, 4, 2]),  # Сортировка по возрастанию (старые сначала)
    ],
)
def test_sort_by_date(sample_transactions, reverse, expected_order):
    """Тестирование сортировки по разным порядкам"""
    result = sort_by_date(sample_transactions, reverse=reverse)
    assert [t["id"] for t in result] == expected_order


def test_sort_with_same_dates(transactions_with_same_dates):
    """Проверка стабильности сортировки при одинаковых датах"""
    result = sort_by_date(transactions_with_same_dates)
    # Должны сохраниться исходный порядок при одинаковых датах
    assert [t["id"] for t in result] == [1, 2, 3]


@pytest.mark.parametrize(
    "invalid_date",
    [
        {"id": 1, "date": "invalid-date-format"},  # Неправильный формат
        {"id": 2, "date": "2023/08/15"},  # Нестандартный формат
        {"id": 3, "date": ""},  # Пустая строка
        {"id": 4, "date": None},  # None вместо даты
        {"id": 5},  # Отсутствует ключ date
    ],
)
def test_invalid_date_formats(invalid_date):
    """Проверка обработки некорректных форматов дат"""
    with pytest.raises((ValueError, KeyError, TypeError)):
        sort_by_date([invalid_date])
