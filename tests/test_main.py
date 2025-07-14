import pytest
from unittest.mock import patch, mock_open
from main import print_transaction, get_user_choice, get_user_input, main
from typing import List, Dict
import json

# Тестовые данные
SAMPLE_TRANSACTION = {
    "date": "2023-01-01",
    "description": "Payment",
    "from": "Card 1234",
    "to": "Account 5678",
    "amount": "100.00",
    "currency": "RUB"
}

SAMPLE_TRANSACTION_NO_FROM = {
    "date": "2023-01-02",
    "description": "Deposit",
    "to": "Account 5678",
    "amount": "200.00",
    "currency": "USD"
}


# Тесты для print_transaction
def test_print_transaction_full(capsys):
    print_transaction(SAMPLE_TRANSACTION)
    captured = capsys.readouterr()
    assert "2023-01-01 Payment" in captured.out
    assert "Card 1234 -> Account 5678" in captured.out
    assert "Сумма: 100.00 руб." in captured.out


def test_print_transaction_no_from(capsys):
    print_transaction(SAMPLE_TRANSACTION_NO_FROM)
    captured = capsys.readouterr()
    assert "Account 5678" in captured.out
    assert "Сумма: 200.00 USD" in captured.out


def test_print_transaction_invalid_data(capsys):
    print_transaction("invalid data")
    captured = capsys.readouterr()
    assert "Ошибка: неверный формат транзакции" in captured.out


# Тесты для get_user_choice
def test_get_user_choice_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "2")
    result = get_user_choice("Prompt", ["Option1", "Option2", "Option3"])
    assert result == "Option2"


def test_get_user_choice_invalid_then_valid(monkeypatch):
    inputs = iter(["invalid", "3"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = get_user_choice("Prompt", ["A", "B", "C"])
    assert result == "C"


# Тесты для get_user_input
def test_get_user_input_valid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "yes")
    result = get_user_input("Prompt", ["yes", "no"])
    assert result == "yes"


def test_get_user_input_no_validation(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "anything")
    result = get_user_input("Prompt")
    assert result == "anything"


# Интеграционные тесты для main
@patch('main.load_transactions_json')
@patch('main.filter_by_state')
@patch('main.sort_by_date')
@patch('main.process_bank_operations')
@patch('main.process_bank_search')
def test_main_full_flow(
        mock_search, mock_operations, mock_sort,
        mock_filter, mock_load, capsys
):
    # Настройка моков
    mock_load.return_value = [SAMPLE_TRANSACTION, SAMPLE_TRANSACTION_NO_FROM]
    mock_filter.return_value = [SAMPLE_TRANSACTION]
    mock_sort.return_value = [SAMPLE_TRANSACTION]
    mock_operations.return_value = [SAMPLE_TRANSACTION]
    mock_search.return_value = [SAMPLE_TRANSACTION]

    # Эмулируем пользовательский ввод
    inputs = [
        "1",  # Выбор JSON
        "EXECUTED",  # Статус
        "да",  # Сортировать
        "по возрастанию",  # Порядок
        "да",  # Только рубли
        "нет"  # Не фильтровать по описанию
    ]

    with patch('builtins.input', side_effect=inputs):
        main()

    captured = capsys.readouterr()
    assert "Для обработки выбран JSON-файл" in captured.out
    assert "Операции отфильтрованы по статусу" in captured.out
    assert "Распечатываю итоговый список транзакций" in captured.out


@patch('main.load_transactions_json')
def test_main_empty_transactions(mock_load, capsys):
    mock_load.return_value = []
    with patch('builtins.input', return_value="1"):
        main()
    captured = capsys.readouterr()
    assert "Ошибка: загруженные данные имеют неверный формат" in captured.out


@patch('main.load_transactions_json')
def test_main_invalid_status(mock_load, capsys):
    mock_load.return_value = [SAMPLE_TRANSACTION]
    inputs = ["1", "INVALID", "EXECUTED", "нет", "нет", "нет"]

    with patch('builtins.input', side_effect=inputs):
        main()

    captured = capsys.readouterr()
    assert "Статус операции \"INVALID\" недоступен" in captured.out


# Тест для обработки ошибок загрузки файла
@patch('main.load_transactions_json')
def test_main_file_load_error(mock_load, capsys):
    mock_load.side_effect = Exception("File not found")
    with patch('builtins.input', return_value="1"):
        main()
    captured = capsys.readouterr()
    assert "Ошибка при загрузке файла" in captured.out


# Тест для пустого результата после фильтрации
@patch('main.load_transactions_json')
@patch('main.filter_by_state')
def test_main_empty_filter_result(mock_filter, mock_load, capsys):
    mock_load.return_value = [SAMPLE_TRANSACTION]
    mock_filter.return_value = []
    inputs = ["1", "EXECUTED", "нет", "нет", "нет"]  # Добавлены ответы на все вопросы

    with patch('builtins.input', side_effect=inputs):
        main()

    captured = capsys.readouterr()
    assert "Не найдено ни одной транзакции" in captured.out