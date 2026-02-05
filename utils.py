from datetime import datetime


def validate_date(date_str: str):
    date_str = date_str.strip()
    # проверка
    try:
        datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except(ValueError, TypeError):
        return False
