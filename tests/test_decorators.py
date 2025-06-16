import pytest

from src.decorators import log


# Тест для логирования в файл (успешное выполнение)
def test_log_to_file_success(log_file):
    @log(filename=log_file)
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5

    with open(log_file, "r") as f:
        content = f.read()
        assert "add ok" in content


# Тест для логирования в файл (ошибка)
def test_log_to_file_error(log_file):
    @log(filename=log_file)
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    with open(log_file, "r") as f:
        content = f.read()
        # Проверяем ключевые части сообщения
        assert "divide error: ZeroDivisionError" in content
        assert "args: (1, 0)" in content
        assert "kwargs: {}" in content
        assert "error: division by zero" in content


# Тест для логирования в консоль (успешное выполнение)
def test_log_to_console_success(capsys):
    @log()
    def multiply(a, b):
        return a * b

    result = multiply(3, 4)
    assert result == 12

    captured = capsys.readouterr()
    assert "multiply ok" in captured.out


# Тест для логирования в консоль (ошибка)
def test_log_to_console_error(capsys):
    @log()
    def fail():
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        fail()

    captured = capsys.readouterr()
    # Проверяем ключевые части сообщения
    assert "fail error: ValueError" in captured.out
    assert "args: ()" in captured.out
    assert "kwargs: {}" in captured.out
    assert "error: Test error" in captured.out


# Тест для проверки сохранения имени функции
def test_function_name_preserved():
    @log()
    def original_name():
        pass

    assert original_name.__name__ == "original_name"


def test_log_with_kwargs(log_file):
    @log(filename=log_file)
    def greet(name, title=None):
        if title is not None and not isinstance(title, str):
            raise TypeError("Title must be a string")
        return f"Hello, {name}"

    # 1. Тестируем успешный вызов без title
    result = greet("Evgeniy", title=None)
    assert result == "Hello, Evgeniy"

    # Проверяем лог успешного вызова
    with open(log_file, "r") as f:
        log_content = f.read()
        assert "greet ok" in log_content
        assert "kwargs: {'title': None}" in log_content  # Проверяем None в kwargs
        assert "result: Hello, Evgeniy" in log_content

    # 2. Тестируем успешный вызов с title (хотя он не используется)
    result = greet("Evgeniy", title=None)
    assert result == "Hello, Evgeniy"

    with open(log_file, "r") as f:
        log_content = f.read()
        assert "kwargs: {'title': None}" in log_content

    # 3. Тестируем вызов с ошибкой
    with pytest.raises(TypeError):
        greet("Evgeniy", title=123)

    with open(log_file, "r") as f:
        log_content = f.read()
        assert "greet error" in log_content
        assert "TypeError" in log_content
        assert "kwargs: {'title': 123}" in log_content
