"""The messages router module"""

from fastapi import (
    APIRouter,
    Depends,
    responses,
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
    Union,
)

from app.auth import (
    schemas as auth_schemas,
)
from app.config import (
    settings,
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

# deta = Deta(settings().DETA_PROJECT_KEY)

# sent_images = deta.Drive("sent-images")

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
) -> Union[Dict[str, Any], str]:
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


@router.get("/chat/images/user/{user_id}/{uuid_val}")
async def get_sent_user_chat_images(
    user_id: str, uuid_val: str
) -> responses.StreamingResponse:
    """
    The get_sent_user_chat_images endpoint.

    Args:
        user_id (id) : The id of the sender of the image.
        uuid_val (str): A unique uuid generated upon upload.

    Returns:
        responses: return a response object for a given url(image).
    """
    try:
        # img = sent_images.get(f"/chat/images/user/{user_id}/{uuid_val}")
        return responses.StreamingResponse(
            [].iter_chunks(), media_type="image/png" # type: ignore
        )
    except Exception:  # pylint: disable=W0703
        return {"status_code": 400, "message": "Something went wrong!"}


@router.get(
    "/message/users",
    response_model=users_schemas.UsersSchema,
    status_code=200,
    name="messages:get-all-messages",
    responses={
        200: {
            "model": users_schemas.UsersSchema,
            "description": "Return a list of users sent/received messages"
            " to/from the authenticated user.",
        },
    },
)
async def get_conversation_users(
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Return all users sent messages to this authenticated user.
    """
    results = await messages_crud.get_all_users_messages(
        current_user.id, session
    )
    return results
