from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""
    if not account_info.strip():
        return account_info

    parts = account_info.split()
    if not parts:
        return account_info

    # Обработка счета
    if parts[0] == "Счет":
        if len(parts) < 2:
            return account_info
        try:
            account_number = parts[-1]
            masked_number = get_mask_account(account_number)
            return f"Счет {masked_number}"
        except ValueError:
            return account_info

    # Обработка карты (проверяем, есть ли номер карты в конце)
    elif len(parts) > 1 and parts[-1].isdigit():
        try:
            card_name = " ".join(parts[:-1])
            card_number = parts[-1]
            masked_number = get_mask_card_number(card_number)
            return f"{card_name} {masked_number}"
        except ValueError:
            return account_info

    # Неизвестный формат
    return account_info


if __name__ == "__main__":
    result = mask_account_card("MasterCard 7158300734726758")
    print(result)


def get_date(date_info: str) -> str:
    """Преобразует строку с датой в строку формата 'ДД.ММ.ГГГГ'."""
    if not date_info:
        raise ValueError("Пустая строка не допускается.")

    # Пытаемся распарсить дату в разных форматах
    try:
        # Пробуем ISO-формат (2024-03-11 или 2024-03-11T12:30:45)
        dt = datetime.fromisoformat(date_info.replace(" ", "T"))
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        try:
            # Пробуем другой возможный формат (например, 2024-03-11 12:30:45)
            dt = datetime.strptime(date_info, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%d.%m.%Y")
        except ValueError:
            raise ValueError(
                "Некорректный формат даты. Ожидается 'ГГГГ-ММ-ДД', 'ГГГГ-ММ-ДДTЧЧ:ММ:СС' или 'ГГГГ-ММ-ДД ЧЧ:ММ:СС'"
            )


if __name__ == "__main__":
    result = get_date("2024-03-11T02:26:18.671407")
    print(result)
