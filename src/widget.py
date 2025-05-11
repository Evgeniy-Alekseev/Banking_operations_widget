import os
from masks import get_mask_card_number
from masks import get_mask_account

def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в переданной строке."""
    parts = account_info.split()
    if not parts:
        return account_info
    if parts[0] == "Счет": # Маскируем номер счета
        account_number = parts[-1]
        masked_number = get_mask_account(account_number)
        return f"Счет {masked_number}"
    else:# Маскируем номер карты
        card_name = ' '.join(parts[:-1])
        card_number = parts[-1]
        masked_number = get_mask_card_number(card_number)
        return f"{card_name} {masked_number}"

if __name__ == '__main__':
    result = mask_account_card('MasterCard 7158300734726758')
    print(result)



def get_date(date_info: str) -> str:
    """Преобразует строку с датой в строку формата 'ДД.ММ.ГГГГ'."""
    date_part = date_info.split('T')[0]  # Получаем "2024-03-11"
    year, month, day = date_part.split('-')
    return f"{day}.{month}.{year}"


if __name__ == '__main__':
    result = get_date('2024-03-11T02:26:18.671407')
    print(result)
