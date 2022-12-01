"""The utils dependencies module."""

from odmantic.session import (
    AIOSession,
)
from starlette.requests import (
    Request,
)
from typing import (
    AsyncGenerator,
)


async def get_db_transactional_session(
    request: Request,
) -> AsyncGenerator[AIOSession, None]:
    """
    Create and get an engine session.

    Args:
        request (starlette.requests.Request): current request.
    Yields :
        odmantic.session.AIOSession: a database session.
    """
    try:
        session: AIOSession = request.app.state.engine.session()
        await session.start()
        yield session
    finally:
        await session.end()


async def get_db_autocommit_session() -> AsyncGenerator[AIOSession, None]:
    """
    Create and get database session.

    Args:
        request (starlette.requests.Request): current request.
    Yields :
        odmantic.session.AIOSession: a database session.
    """

    from app.main import (  # pylint: disable=C0415
        tinder_app,
    )

    try:
        session: AIOSession = tinder_app.state.engine.session()
        await session.start()
        yield session
    finally:
        await session.end()
