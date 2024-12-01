"""Entrypoint for Deta Micros"""

from sys import path

path.append(".")

from app.main import (
    get_app,
    serve,
)

app = get_app()

if __name__ == "__main__":
    serve()
