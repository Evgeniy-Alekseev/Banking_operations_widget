from src.services import process_bank_search, process_bank_operations


# тесты для process_bank_search

def test_search_with_match(sample_transactions):
    # Поиск с учётом регистра
    result = process_bank_search(sample_transactions, "Payment")
    assert len(result) == 1
    assert result[0]["id"] == 3

def test_search_no_match(sample_transactions):
    # Нет совпадений
    result = process_bank_search(sample_transactions, "Bonus")
    assert len(result) == 1

def test_search_partial_match(sample_transactions):
    # Частичное совпадение
    result = process_bank_search(sample_transactions, "pay")
    assert len(result) == 1  # "Salary", "payment", "salary"
    assert {t["id"] for t in result} == {3,}  # Проверка ID

def test_search_empty_string(sample_transactions):
    # Пустая строка поиска
    result = process_bank_search(sample_transactions, "")
    assert len(result) == 0

def test_search_special_chars(sample_transactions):
    # Спецсимволы в поиске
    result = process_bank_search(sample_transactions, "2023")
    assert len(result) == 1
    assert result[0]["id"] == 3

def test_missing_description_key(sample_transactions):
    # Транзакция без ключа 'description'
    result = process_bank_search(sample_transactions, "rent")
    assert len(result) == 3
    assert result[0]["id"] == 4

def test_case_sensitivity(sample_transactions):
    # Проверка чувствительности к регистру
    result = process_bank_search(sample_transactions, "payment")
    assert len(result) == 1  # Без re.IGNORECASE
    assert result[0]["id"] == 3

def test_empty_input():
    assert process_bank_search([], "test") == []


# тесты для process_bank_operations

def test_basic_counting(sample_transactions):
    categories = ["Salary", "Tax"]
    result = process_bank_operations(sample_transactions, categories)
    assert result == {"Salary": 2, "Tax": 1}

def test_empty_categories(sample_transactions):
    assert process_bank_operations(sample_transactions, []) == {}

def test_case_insensitivity(sample_transactions):
    categories = ["salary", "bonus"]
    result = process_bank_operations(sample_transactions, categories)
    assert result == {"salary": 2, "bonus": 1}

def test_missing_description_key():
    transactions = [{"id": 1}, {"id": 2, "description": "Salary"}]
    result = process_bank_operations(transactions, ["Salary"])
    assert result == {"Salary": 1}
