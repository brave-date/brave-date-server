"""The websockets manager module."""

from fastapi import (
    WebSocket,
)
import logging
from typing import (
    List,
)

logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    A websockets connection manager class.
    """

    def __init__(self) -> None:
        """
        A constructor to initialize a `active_connections` variable
        that keeps track of all active websockets.

        Args:
            self ( _obj_ ) : object reference.
        """
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """
        A method that accepts a websocket connection and add it into `active_connections`.

        Args:
            self ( _obj_ ) : object reference.
            websocket ( fastapi.WebSocket ) : websocket object.
        """
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        """
        A method that disconnect a websocket and remove it into `active_connections`.

        Args:
            self ( _obj_ ) : object reference.
            websocket ( fastapi.WebSocket ) : websocket object.
        """
        if self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        """
        A method that broadcasts a message to all `active_connections`.

        Args:
            self ( _obj_ ) : object reference.
            message ( str ) : text message.
        """
        logger.debug(
            "Broadcasting across %s CONNECTIONS", len(self.active_connections)
        )
        for connection in self.active_connections:
            await connection.send_text(message)
            logger.debug("Broadcasting: %s", message)
