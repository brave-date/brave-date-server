# Entrypoint for Deta Micros
from sys import path

path.append(".")

from app.main import (
    get_app,
)

app = get_app()
