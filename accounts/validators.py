import re
from datetime import datetime, date

from django.core.exceptions import ValidationError


def validate_username(username: str) -> None:
    if re.search(r"^[a-zA-Z_]*$", username) is None:
        raise ValidationError(
            f"{username} contains non-english letters or characters other than underscore"
        )
    if username.startswith('_') or username.endswith('_'):
        raise ValidationError(f"{username} cannot start or end with an underscore")


def validate_name(name: str) -> None:
    if re.search(r"^[a-zA-Z]*$", name) is None:
        raise ValidationError(
            f"{name} contains non-english letters"
        )


def validate_birth_date(birth_date: datetime) -> None:
    if birth_date.year < 1900:
        raise ValidationError("Invalid birth date - year must be greater then 1900")

    age = (date.today() - birth_date).days // 365
    if age < 18:
        raise ValidationError("You must be at least 18 years old to register")


def validate_password_strength(password: str) -> None:
    if len(password) < 8:
        raise ValidationError('Password must contain at least 8 characters')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter')
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one digit')
    if not re.search(r'[!@#$%&*]', password):
        raise ValidationError('Password must contain at least one special character')


def validate_file_size(file):
    filesize = file.size
    max_upload_size = 1 * 1024 * 1024

    if filesize > max_upload_size:
        raise ValidationError('The maximus image size that can be uploaded is 1 MB')
    return file
