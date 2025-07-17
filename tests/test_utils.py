import json
import pytest
from unittest.mock import mock_open, patch
from src.utils import load_transactions_json


def test_load_valid_file(tmp_path, sample_data):
    file = tmp_path / "transactions.json"
    file.write_text(json.dumps(sample_data))

    result = load_transactions_json(str(file))
    assert result == sample_data


@pytest.mark.parametrize(
    "content,expected",
    [
        ("", []),  # Пустой файл
        ("{}", []),  # Не список
        ("invalid json", []),  # Невалидный JSON
        ("42", []),  # Число вместо списка
    ],
)
def test_load_invalid_files(tmp_path, content, expected):
    file = tmp_path / "invalid.json"
    file.write_text(content)

    assert load_transactions_json(str(file)) == expected


def test_file_not_found():
    assert load_transactions_json("nonexistent.json") == []


@patch("builtins.open", side_effect=PermissionError)
def test_no_permission(mock_open):
    assert load_transactions_json("restricted.json") == []
