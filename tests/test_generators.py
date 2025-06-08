import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# тесты для filter_by_currency


def test_empty_transactions():
    """Тест с пустым списком транзакций"""
    result = list(filter_by_currency([], "USD"))
    assert len(result) == 0


def test_generator_behavior(transactions_fixture):
    """Тест поведения генератора"""
    generator = filter_by_currency(transactions_fixture, "USD")

    # Проверяем первую транзакцию
    first = next(generator)
    assert first["id"] == 939719570

    # Проверяем вторую транзакцию
    second = next(generator)
    assert second["id"] == 142264268

    # Проверяем StopIteration
    with pytest.raises(StopIteration):
        next(generator)
        next(generator)  # Двойной вызов для проверки


def test_malformed_transactions():
    """Тест с некорректными данными транзакций"""
    malformed = [
        {"id": 1},  # Нет operationAmount
        {"id": 2, "operationAmount": {}},  # Нет currency
        {"id": 3, "operationAmount": {"currency": {}}},  # Нет code
        {"id": 4, "operationAmount": {"currency": {"code": "USD"}}},
    ]

    result = list(filter_by_currency(malformed, "USD"))
    assert len(result) == 1
    assert result[0]["id"] == 4


# Использование параметризации для filter_by_currency


@pytest.mark.parametrize(
    "currency,expected_ids",
    [
        ("USD", [939719570, 142264268, 895315941]),  # Транзакции в USD
        ("RUB", [873106923, 594226727]),  # Транзакции в RUB
        ("EUR", []),  # Нет транзакций в EUR
        ("GBP", []),  # Нет транзакций в GBP
    ],
)
def test_filter_by_currency_with_params(transactions_fixture, currency, expected_ids):
    """Параметризованный тест для разных валют"""
    filtered = list(filter_by_currency(transactions_fixture, currency))
    assert len(filtered) == len(expected_ids)
    assert all(t["id"] in expected_ids for t in filtered)


# тесты для transaction_descriptions


def test_empty_transactions(empty_transactions_fixture):
    """Тест с пустым списком транзакций"""
    generator = transaction_descriptions(empty_transactions_fixture)
    assert list(generator) == []


def test_transactions_without_descriptions(no_description_transactions_fixture):
    """Тест с транзакциями без описаний"""
    generator = transaction_descriptions(no_description_transactions_fixture)
    descriptions = list(generator)
    assert len(descriptions) == 1  # Только одна транзакция с description != None
    assert descriptions[0] is None


def test_generator_behavior(transactions_fixture):
    """Тест поведения генератора"""
    generator = transaction_descriptions(transactions_fixture)

    # Проверяем поочередное получение значений
    assert next(generator) == "Перевод организации"
    assert next(generator) == "Перевод со счета на счет"
    assert next(generator) == "Перевод со счета на счет"
    assert next(generator) == "Перевод с карты на карту"
    assert next(generator) == "Перевод организации"

    # Проверяем завершение генератора
    with pytest.raises(StopIteration):
        next(generator)


# Использование параметризации для transaction_descriptions


@pytest.mark.parametrize(
    "index,expected_description",
    [
        (0, "Перевод организации"),
        (1, "Перевод со счета на счет"),
        (2, "Перевод со счета на счет"),
        (3, "Перевод с карты на карту"),
        (4, "Перевод организации"),
    ],
)
def test_transaction_descriptions_correct_output(transactions_descriptions_fixture, index, expected_description):
    """Тест корректности возвращаемых описаний"""
    generator = transaction_descriptions(transactions_descriptions_fixture)
    descriptions = list(generator)
    assert descriptions[index] == expected_description


@pytest.mark.parametrize(
    "input_data,expected",
    [
        ([], []),
        ([{"description": "Test"}], ["Test"]),
        ([{"description": "A"}, {"description": "B"}], ["A", "B"]),
        ([{"no_description": "Test"}], []),
        ([{"description": None}], [None]),
    ],
)
def test_parametrized_cases(input_data, expected):
    """Параметризованный тест различных случаев"""
    assert list(transaction_descriptions(input_data)) == expected


# тесты для card_number_generator


def test_large_range(card_number_generator_fixture):
    """Тест большого диапазона с проверкой первого и последнего элемента"""
    start = 1
    stop = 100000
    generator = card_number_generator(start, stop)

    # Получаем первый элемент
    first = next(generator)
    assert first == "0000 0000 0000 0001"

    # Получаем последний элемент
    last = None
    count = 1  # Уже получили первый элемент

    for last in generator:
        count += 1

    # Проверяем количество сгенерированных элементов
    assert count == stop - start + 1

    # Проверяем формат последнего элемента
    assert last == "0000 0000 0010 0000"


def test_generator_behavior(card_number_generator_fixture):
    """Тест поведения генератора (пошаговая выдача)"""
    generator = card_number_generator(1, 3)

    assert next(generator) == "0000 0000 0000 0001"
    assert next(generator) == "0000 0000 0000 0002"
    assert next(generator) == "0000 0000 0000 0003"

    # Проверяем завершение генератора
    with pytest.raises(StopIteration):
        next(generator)


# Использование параметризации для card_number_generator


@pytest.mark.parametrize(
    "start,stop,expected",
    [
        # Стандартные случаи
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        # Крайние значения
        (0, 0, ["0000 0000 0000 0000"]),
        (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
        # Диапазон из одного значения
        (1234123412341234, 1234123412341234, ["1234 1234 1234 1234"]),
        # Большой диапазон (проверка только первого и последнего)
        (
            1,
            100,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
                "0000 0000 0000 0006",
                "0000 0000 0000 0007",
                "0000 0000 0000 0008",
                "0000 0000 0000 0009",
                "0000 0000 0000 0010",
                "0000 0000 0000 0011",
                "0000 0000 0000 0012",
                "0000 0000 0000 0013",
                "0000 0000 0000 0014",
                "0000 0000 0000 0015",
                "0000 0000 0000 0016",
                "0000 0000 0000 0017",
                "0000 0000 0000 0018",
                "0000 0000 0000 0019",
                "0000 0000 0000 0020",
                "0000 0000 0000 0021",
                "0000 0000 0000 0022",
                "0000 0000 0000 0023",
                "0000 0000 0000 0024",
                "0000 0000 0000 0025",
                "0000 0000 0000 0026",
                "0000 0000 0000 0027",
                "0000 0000 0000 0028",
                "0000 0000 0000 0029",
                "0000 0000 0000 0030",
                "0000 0000 0000 0031",
                "0000 0000 0000 0032",
                "0000 0000 0000 0033",
                "0000 0000 0000 0034",
                "0000 0000 0000 0035",
                "0000 0000 0000 0036",
                "0000 0000 0000 0037",
                "0000 0000 0000 0038",
                "0000 0000 0000 0039",
                "0000 0000 0000 0040",
                "0000 0000 0000 0041",
                "0000 0000 0000 0042",
                "0000 0000 0000 0043",
                "0000 0000 0000 0044",
                "0000 0000 0000 0045",
                "0000 0000 0000 0046",
                "0000 0000 0000 0047",
                "0000 0000 0000 0048",
                "0000 0000 0000 0049",
                "0000 0000 0000 0050",
                "0000 0000 0000 0051",
                "0000 0000 0000 0052",
                "0000 0000 0000 0053",
                "0000 0000 0000 0054",
                "0000 0000 0000 0055",
                "0000 0000 0000 0056",
                "0000 0000 0000 0057",
                "0000 0000 0000 0058",
                "0000 0000 0000 0059",
                "0000 0000 0000 0060",
                "0000 0000 0000 0061",
                "0000 0000 0000 0062",
                "0000 0000 0000 0063",
                "0000 0000 0000 0064",
                "0000 0000 0000 0065",
                "0000 0000 0000 0066",
                "0000 0000 0000 0067",
                "0000 0000 0000 0068",
                "0000 0000 0000 0069",
                "0000 0000 0000 0070",
                "0000 0000 0000 0071",
                "0000 0000 0000 0072",
                "0000 0000 0000 0073",
                "0000 0000 0000 0074",
                "0000 0000 0000 0075",
                "0000 0000 0000 0076",
                "0000 0000 0000 0077",
                "0000 0000 0000 0078",
                "0000 0000 0000 0079",
                "0000 0000 0000 0080",
                "0000 0000 0000 0081",
                "0000 0000 0000 0082",
                "0000 0000 0000 0083",
                "0000 0000 0000 0084",
                "0000 0000 0000 0085",
                "0000 0000 0000 0086",
                "0000 0000 0000 0087",
                "0000 0000 0000 0088",
                "0000 0000 0000 0089",
                "0000 0000 0000 0090",
                "0000 0000 0000 0091",
                "0000 0000 0000 0092",
                "0000 0000 0000 0093",
                "0000 0000 0000 0094",
                "0000 0000 0000 0095",
                "0000 0000 0000 0096",
                "0000 0000 0000 0097",
                "0000 0000 0000 0098",
                "0000 0000 0000 0099",
                "0000 0000 0000 0100",
            ],
        ),
    ],
)
def test_card_number_generator_range(card_number_generator_fixture, start, stop, expected):
    """Тест генерации номеров в заданном диапазоне"""
    generator = card_number_generator(start, stop)
    result = list(generator)

    # Для больших диапазонов проверяем только первый и последний элементы
    if len(expected) > 5 and expected[1] == ...:
        assert result[0] == expected[0]
        assert result[-1] == expected[-1]
        assert len(result) == stop - start + 1
    else:
        assert result == expected


@pytest.mark.parametrize(
    "number,formatted",
    [
        (0, "0000 0000 0000 0000"),
        (1, "0000 0000 0000 0001"),
        (9999, "0000 0000 0000 9999"),
        (1234567812345678, "1234 5678 1234 5678"),
        (9999999999999999, "9999 9999 9999 9999"),
    ],
)
def test_card_number_formatting(card_number_generator_fixture, number, formatted):
    """Тест корректности форматирования номеров карт"""
    generator = card_number_generator(number, number)
    assert next(generator) == formatted


@pytest.mark.parametrize(
    "start,stop,expected_error",
    [
        (-1, 5, "Параметры не могут быть отрицательными"),  # Отрицательный start
        (5, 1, "Начальное значение должно быть меньше или равно конечному"),  # start > stop
        (0, 10000000000000000, "Максимальное значение - 9999999999999999"),  # Превышение максимума
        ("1", 5, "Параметры должны быть целыми числами"),  # Нечисловые параметры
        (1.5, 5, "Параметры должны быть целыми числами"),  # Дробные числа
    ],
)
def test_invalid_ranges(card_number_generator_fixture, start, stop, expected_error):
    """Тест обработки невалидных диапазонов"""
    with pytest.raises(ValueError) as exc_info:
        list(card_number_generator(start, stop))
    assert expected_error in str(exc_info.value)
