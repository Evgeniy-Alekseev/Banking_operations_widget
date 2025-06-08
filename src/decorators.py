from datetime import datetime
from functools import wraps


def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                result = func(*args, **kwargs)
                # Добавляем логирование аргументов и результата
                log_message = f"{timestamp} - {func_name} ok - " f"args: {args}, kwargs: {kwargs}, result: {result}\n"
                if filename:
                    with open(filename, "a") as f:
                        f.write(log_message)
                else:
                    print(log_message, end="")
                return result
            except Exception as e:
                error_message = (
                    f"{timestamp} - {func_name} error: {type(e).__name__} - "
                    f"args: {args}, kwargs: {kwargs}, error: {str(e)}\n"
                )
                if filename:
                    with open(filename, "a") as f:
                        f.write(error_message)
                else:
                    print(error_message, end="")
                raise

        return wrapper

    return decorator
