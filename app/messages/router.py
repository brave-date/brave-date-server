"""The messages router module"""

from fastapi import (
    APIRouter,
    Depends,
)
from odmantic.session import (
    AIOSession,
)
from pydantic import (
    EmailStr,
)
from typing import (
    Any,
    Dict,
)

from app.auth import (
    schemas as auth_schemas,
)
from app.messages import (
    crud as messages_crud,
    schemas as messages_schemas,
)
from app.users import (
    schemas as users_schemas,
)
from app.utils import (
    dependencies,
    jwt,
)

router = APIRouter(prefix="/api/v1")


@router.post(
    "/message",
    response_model=auth_schemas.ResponseSchema,
    status_code=201,
    name="chats:send-message",
    responses={
        201: {
            "model": auth_schemas.ResponseSchema,
            "description": "Message has been delivered successfully!",
        },
        401: {
            "model": auth_schemas.ResponseSchema,
            "description": "Empty message, non existing receiver!",
        },
    },
)
async def send_message(
    request: messages_schemas.MessageCreate,
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Deliver a new message given an authenticated user.
    """
    results = await messages_crud.send_new_message(
        current_user.id, request, None, session
    )
    return results


@router.get(
    "/message",
    response_model=messages_schemas.GetAllMessageResults,
    status_code=200,
    name="messages:get-all-messages",
    responses={
        200: {
            "model": messages_schemas.GetAllMessageResults,
            "description": "Return a list of messages between two users.",
        },
    },
)
async def get_conversation(
    receiver: EmailStr,
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Return all messages grouped by senders for a given receiver.
    """
    results = await messages_crud.get_sender_receiver_messages(
        current_user.id, receiver, session
    )
    return results
