import hashlib


def create_gravatar_url(email: str, size: int = 100) -> str:
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    url = f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"
    return url


def get_user_directory_path(instance, filename) -> str:
    return f'avatars/{instance.user.username}/{filename}'
