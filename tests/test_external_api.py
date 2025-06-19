import pytest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv
from src.external_api import get_amount_in_rub


@pytest.mark.parametrize("transaction,expected", [
    ({"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}, 100.0),
    ({"operationAmount": {"amount": "100", "currency": {"code": "USD"}}}, 7550.0),  # При курсе 75.5
    ({"operationAmount": {"amount": "50.5", "currency": {"code": "RUB"}}}, 50.5),
    ({}, 0.0),  # Нет данных
    ({"operationAmount": {"amount": "100"}}, 0.0),  # Нет валюты
    ({"operationAmount": {"currency": {"code": "RUB"}}}, 0.0),  # Нет суммы
])
@patch('requests.get')
def test_get_amount_in_rub(mock_get, transaction, expected):
    # Настраиваем мок для API
    if transaction.get('operationAmount', {}).get('currency', {}).get('code') == 'USD':
        mock_response = MagicMock()
        mock_response.json.return_value = {'rates': {'RUB': 75.50}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

    assert get_amount_in_rub(transaction) == expected

import pytest
from unittest.mock import patch, MagicMock
import requests
from src.external_api import get_amount_in_rub

# Тестовый API ключ
TEST_API_KEY = "test_api_key_123"

@patch('requests.get')
@patch('src.external_api.API_KEY', TEST_API_KEY)  # Мокаем API_KEY
def test_usd_conversion(mock_get):
    # 1. Настраиваем мок для успешного ответа API
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'rates': {'RUB': 75.50},
        'success': True
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # 2. Подготавливаем тестовые данные
    transaction = {
        "operationAmount": {
            "amount": "100",
            "currency": {
                "code": "USD"
            }
        }
    }

    # 3. Вызываем тестируемую функцию
    result = get_amount_in_rub(transaction)

    # 4. Проверяем результаты
    assert result == 7550.0  # 100 * 75.50

    # 5. Проверяем вызов API
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        params={'base': 'USD', 'symbols': 'RUB'},
        headers={'apikey': TEST_API_KEY},
        timeout=10
    )
