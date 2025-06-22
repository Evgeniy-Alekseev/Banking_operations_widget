import json
from unittest.mock import mock_open, patch

import pytest

from src.utils import load_transactions


def test_load_valid_file(tmp_path, sample_data):
    file = tmp_path / "transactions.json"
    file.write_text(json.dumps(sample_data))

    result = load_transactions(str(file))
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

    assert load_transactions(str(file)) == expected


def test_file_not_found():
    assert load_transactions("nonexistent.json") == []


@patch("builtins.open", side_effect=PermissionError)
def test_no_permission(mock_open):
    assert load_transactions("restricted.json") == []
