def validate_amount(amount):
    """
    Validate if the amount is a positive number.
    """
    if isinstance(amount, (int, float)) and amount > 0:
        return True
    return False


def validate_date(date_str):
    """
    Validate if the date is in YYYY-MM-DD format.
    """
    from datetime import datetime
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
