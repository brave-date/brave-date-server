"""The utils crypt module."""

from passlib.context import (
    CryptContext,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash using the bcrypt algorithm.
    Args:
        plain_password (str): The password to verify.
        hashed_password (str): The hashed password to verify against.
    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a password using the bcrypt algorithm.
    Args:
        password (str): The password to hash.
    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)
