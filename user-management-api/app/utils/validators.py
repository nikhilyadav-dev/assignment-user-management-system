import re


EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def is_valid_email(email):
    return re.match(EMAIL_PATTERN, email) is not None