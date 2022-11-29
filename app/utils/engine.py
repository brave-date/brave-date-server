"""The utils engine module."""

from fastapi import (
    FastAPI,
)
from motor.motor_asyncio import (
    AsyncIOMotorClient,
)
from odmantic import (
    AIOEngine,
)

from app.config import (
    settings,
)


async def init_engine_app(app: FastAPI) -> None:
    """
    Creates database and connections to the database.

    This function creates a mongodb client instance,
    and an odmantic engine and stores them in the
    application's state property.

    Args:
        app (fastapi.FastAPI): fastAPI application.
    """
    app_settings = settings()

    client = AsyncIOMotorClient(
        app_settings.db_url, maxPoolSize=30, minPoolSize=30
    )
    database = client.get_default_database()
    assert database.name == app_settings.MONGODB_DATABASE
    engine = AIOEngine(client=client, database="tinder")
    app.state.client = client
    app.state.engine = engine
