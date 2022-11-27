"""
A fully async based server for Brave Date built using FastAPI,
MongoDB, pydantic, Motor, Redis, and Deta.
"""


__author__ = """Mahmoud Harmouch"""
__email__ = "business@wiseai.com"
__version__ = "0.1.0"


from app import (
    auth,
    users,
    utils,
)

__all__ = [
    "auth",
    "users",
    "utils",
]
