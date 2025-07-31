import re


def validate_phone_number(phone_number):
    pattern = r'^\+998[0-9]{9}$'
    if re.match(pattern, phone_number):
        return True
    return False


def validate_name(name):
    # Simple validation for name: must be alphabetic and at least 2 characters long
    return name.isalpha() and len(name) >= 2
