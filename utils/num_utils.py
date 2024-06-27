import re


def currency_to_float(currency_str):
    # Use regex to remove any non-numeric characters except for the decimal point
    numeric_str = re.sub(r'[^\d.]', '', currency_str)
    try:
        return float(numeric_str)
    except ValueError:
        raise ValueError(f"Cannot convert {currency_str} to float")
