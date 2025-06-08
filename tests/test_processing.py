import sys
from pathlib import Path

import pytest

from src.processing import filter_by_state, sort_by_date

sys.path.append(str(Path(__file__).parent.parent))


# тесты для filter_by_state
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


# Использование параметризации для filter_by_state
@pytest.mark.parametrize(
    "state, expected_ids",
    [
        ("EXECUTED", [1, 3, 5]),
        ("PENDING", [2]),
        ("CANCELED", [4]),
    ],
)
def test_filter_by_state(sample_transactions, state, expected_ids):
    result = filter_by_state(sample_transactions, state)
    assert [t["id"] for t in result] == expected_ids


# тесты для sort_by_date
def test_edge_cases(edge_case_transactions):
    """Проверка граничных случаев дат"""
    result = sort_by_date(edge_case_transactions)
    assert [t["id"] for t in result] == [2, 3, 1]  # По умолчанию сортировка по убыванию


def test_mixed_valid_invalid(mixed_transactions):
    """Проверка работы со смешанными валидными и невалидными данными"""
    with pytest.raises((ValueError, KeyError)):
        sort_by_date(mixed_transactions)


# Использование параметризации для sort_by_date
@pytest.mark.parametrize(
    "reverse, expected_order",
    [
        (True, [5, 2, 4, 1, 3]),  # По убыванию (новые сначала)
        (False, [3, 1, 4, 2, 5]),  # По возрастанию (старые сначала)
    ],
)
def test_sort_with_different_dates(transactions_with_different_dates, reverse, expected_order):
    """Тестирование сортировки по разным порядкам с разными датами"""
    result = sort_by_date(transactions_with_different_dates, reverse=reverse)
    assert [t["id"] for t in result] == expected_order


def test_stable_sort_with_same_dates(transactions_with_same_dates):
    """Проверка стабильности сортировки при одинаковых датах"""
    result = sort_by_date(transactions_with_same_dates)
    # Должен сохраниться исходный порядок при одинаковых датах
    assert [t["id"] for t in result] == [1, 2, 3]


# Тесты для обработки некорректных данных
@pytest.mark.parametrize(
    "transaction",
    [
        {"id": 1, "date": "invalid-date-format", "state": "EXECUTED"},
        {"id": 2, "date": "2023/08/15", "state": "PENDING"},  # Нестандартный формат
        {"id": 3, "date": "", "state": "CANCELED"},  # Пустая строка
        {"id": 4, "date": None, "state": "EXECUTED"},  # None вместо даты
        {"id": 5, "state": "PENDING"},  # Отсутствует ключ date
    ],
)
def test_invalid_date_handling(transaction):
    """Проверка обработки некорректных форматов дат"""
    with pytest.raises((ValueError, KeyError, TypeError)):
        sort_by_date([transaction])


def test_empty_list():
    """Проверка работы с пустым списком"""
    assert sort_by_date([]) == []


def test_single_transaction():
    """Проверка работы с одним элементом"""
    transaction = [{"id": 1, "date": "2023-08-15T12:00:00", "state": "EXECUTED"}]
    assert sort_by_date(transaction) == transaction
