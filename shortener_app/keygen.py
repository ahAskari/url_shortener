import secrets
import string
from sqlalchemy.orm import Session
from . import crud


def generate_random_key(length: int = 5):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> str:
    key = generate_random_key()
    while crud.get_db_url_by_key(db, key):
        key = generate_random_key()
    return key
