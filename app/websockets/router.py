"""The websockets router module."""

from asyncio import (
    ensure_future,
)
import base64
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.websockets import (
    WebSocket,
)
import json
import logging
from odmantic.session import (
    AIOSession,
)
from starlette.websockets import (
    WebSocketState,
)
from typing import (
    NamedTuple,
)

from app.auth import (
    crud as auth_crud,
)
from app.messages import (
    crud as messages_crud,
)
from app.utils import (
    dependencies,
)
from app.websockets.manager import (
    ConnectionManager,
)


class RequestObject(NamedTuple):
    """
    RequestObject helper class.
    """

    receiver: str
    content: str
    message_type: str
    media: str


logger = logging.getLogger(__name__)

manager = ConnectionManager()


router = APIRouter(prefix="/api/v1")


@router.websocket("/ws/chat/{sender_id}/{receiver_id}")
async def websocket_chat_endpoint(
    websocket: WebSocket,
    sender_id: str,
    receiver_id: str,
    session: AIOSession = Depends(dependencies.get_db_autocommit_session),
) -> None:
    """
    websocket endpoint.
    """
    try:
        # add user
        await manager.connect(websocket)
        sender = await auth_crud.find_existed_user_id(sender_id, session)
        data = {
            "content": f"{sender.first_name} is online!",  # type: ignore
            "type": "online",
            "user": sender,
        }
        await manager.broadcast(json.dumps(data, default=str))
        # wait for messages
        while True:
            if websocket.application_state == WebSocketState.CONNECTED:
                data = await websocket.receive_text()
                message_data = json.loads(data)  # type: ignore
                message_data["user"] = dict(sender)  # type: ignore
                if message_data.get("type", None) == "leave":
                    logger.warning(message_data["content"])
                    data = {
                        "content": f"{sender.first_name} went offline!",  # type: ignore
                        "type": "offline",
                        "user": dict(sender),  # type: ignore
                    }
                    await manager.broadcast(json.dumps(data, default=str))
                    logger.info("Disconnecting from Websocket")
                    await manager.disconnect(websocket)
                    break
                if message_data.get("type", None) == "media":
                    data = message_data.pop("content")
                    bin_photo = base64.b64decode(data)  # type: ignore
                    receiver = await auth_crud.find_existed_user_id(
                        receiver_id, session
                    )
                    request = RequestObject(
                        receiver.email,  # type: ignore
                        "",
                        message_data["type"],
                        message_data,
                    )
                    url = await messages_crud.send_new_message(
                        sender_id, request, bin_photo, session  # type: ignore
                    )
                    message_data["media"] = url
                    message_data["content"] = ""
                    message_data.pop("preview")
                    await manager.broadcast(
                        json.dumps(message_data, default=str)
                    )
                    del request
                else:
                    logger.info(
                        "RECIEVED: %s",
                        json.dumps(message_data, default=str),  # noqa: E501
                    )
                    await manager.broadcast(
                        json.dumps(message_data, default=str)
                    )
                    receiver = await auth_crud.find_existed_user_id(
                        receiver_id, session
                    )
                    request = RequestObject(
                        receiver.email,  # type: ignore
                        message_data["content"],
                        message_data["type"],
                        "",
                    )
                    ensure_future(
                        messages_crud.send_new_message(
                            sender_id, request, None, session  # type: ignore
                        )
                    )
                    del request
            else:
                logger.warning(
                    "Websocket state: %s, reconnecting...",
                    websocket.application_state,
                )
                await manager.connect(websocket)
    except Exception as ex:
        message = f"An exception {ex} occurred. Arguments:\n{ex.args!r}"  # noqa: E231
        logger.error(message)
        logger.warning("Disconnecting Websocket")
        await manager.disconnect(websocket)
