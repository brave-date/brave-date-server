"""The messages crud module"""

from bson import (
    ObjectId,
)
from datetime import (
    datetime,
)
from deta import Deta
import logging
from odmantic.session import (
    AIOSession,
)
from pydantic import (
    EmailStr,
)
from typing import (
    Any,
    Dict,
    Optional,
    Union,
)
import uuid

from app.auth import (
    crud as auth_crud,
)
from app.config import (
    settings,
)
from app.messages import (
    models as messages_models,
    schemas as messages_schemas,
)
from app.users import (
    models as users_models,
)

logger = logging.getLogger(__name__)

deta = Deta(settings().DETA_PROJECT_KEY)

images = deta.Drive("sent-images")


async def send_new_message(
    sender_id: str,
    request: messages_schemas.MessageCreate,
    file: Optional[str],
    session: AIOSession,
) -> Union[Dict[str, Any], str]:
    """
    A method to create a message.

    Args:
        sender_id (str) : A user id for a given message sender.
        request (app.messages.schemas.MessageCreate) : A request schema object.
        file (str) : A base64 file content.
        session (odmantic.session.AIOSession) : odmantic session object.

    Returns:
        Dict[str, Any] | : A Response schema dict or uploaded file name.
    """
    receiver = await auth_crud.find_existed_user(
        email=request.receiver, session=session
    )
    if request.message_type == "media":
        if not request.media["preview"]:  # type: ignore
            return {
                "status_code": 400,
                "message": "You can't upload an empty file!",
            }
        file_name = (
            f"/chat/images/user/{str(sender_id)}/image_{str(uuid.uuid4())}.png"
        )
        images.put(file_name, file)
        # create a new message
        new_message = messages_models.Message(
            content="", message_type="media", media=file_name, status=1
        )
    else:
        if not request.content:
            return {
                "status_code": 400,
                "message": "You can't send an empty message!",
            }
        if not receiver:
            return {
                "status_code": 400,
                "message": "You can't send a message to a non existing"
                " user!",
            }
        if receiver.id == sender_id:
            return {
                "status_code": 400,
                "message": "You can't send a message to yourself!",
            }
        # create a new message
        new_message = messages_models.Message(
            content=request.content,
            message_type=request.message_type,
            media="",
            status=1,
        )
    await session.save(new_message)
    # append the new message into the conversation list; check if conversation exists, first.
    conversation = await session.find_one(
        messages_models.Conversation,
        messages_models.Conversation.sender == ObjectId(sender_id),
        messages_models.Conversation.receiver == ObjectId(receiver.id),
    )
    if not conversation:
        conversation = messages_models.Conversation(
            sender=sender_id, receiver=receiver.id, messages=[new_message.id]
        )
    else:
        messages = conversation.messages
        messages.extend(
            [
                new_message.id,
            ]
        )
        conversation.update(
            {
                "sender": ObjectId(sender_id),
                "receiver": ObjectId(receiver.id),
                "messages": messages,
                "modified_date": datetime.utcnow(),
            }
        )
    await session.save(conversation)
    if request.message_type == "media":
        return file_name
    return {
        "status_code": 201,
        "message": "A new message has been delivered successfully!",
    }


async def get_sender_receiver_messages(
    sender_id: str, receiver: EmailStr, session: AIOSession
) -> Dict[str, Any]:
    """
    A method to create a message.

    Args:
        sender_id (str) : A user id for a given message sender.
        receiver (pydantic.EmailStr) : A given receiver email address.
        session (odmantic.session.AIOSession) : odmantic session object.

    Returns:
        Dict[str, Any]: A Response schema dict.
    """
    receiver = await auth_crud.find_existed_user(
        email=receiver, session=session
    )
    conversation_sent = await session.find_one(
        messages_models.Conversation,
        messages_models.Conversation.sender == sender_id,
        messages_models.Conversation.receiver == receiver.id,
    )
    messages_sent = []
    messages_received = []
    if conversation_sent:
        messages_sent_ids = conversation_sent.messages
        messages_sent_objects = await session.find(
            messages_models.Message,
            messages_models.Message.id.in_(messages_sent_ids),
        )
        for message in messages_sent_objects:
            message_dict = message.dict()
            message_dict["type"] = "sent"
            message_dict["id"] = str(message_dict["id"])
            messages_sent.append(message_dict)
    conversation_received = await session.find_one(
        messages_models.Conversation,
        messages_models.Conversation.sender == receiver.id,
        messages_models.Conversation.receiver == sender_id,
    )
    if conversation_received:
        messages_received_ids = conversation_received.messages
        messages_sent_objects = await session.find(
            messages_models.Message,
            messages_models.Message.id.in_(messages_received_ids),
        )
        for message in messages_sent_objects:
            message_dict = message.dict()
            message_dict["type"] = "received"
            message_dict["id"] = str(message_dict["id"])
            # Mark received message as read
            message_dict["status"] = 0
            messages_received.append(message_dict)
            # pop the id to fix ValueError: Updating the primary key is not supported.
            message_dict.pop("id")
            message.update(message_dict)
            await session.save(message)
        messages_sent.extend(messages_received)
    messages = sorted(
        messages_sent, key=lambda message_dict: message_dict["creation_date"]
    )
    results = {"status_code": 200, "result": messages}
    return results


async def get_all_users_messages(
    sender_id: str, session: AIOSession
) -> Dict[str, Any]:
    """
    A method to get all users sent messages to the authenticated user.

    Args:
        sender_id (str) : A user id for a given message sender.
        session (odmantic.session.AIOSession) : odmantic session object.

    Returns:
        Dict[str, Any]: A Response schema dict.
    """
    conversations_sent = await session.find(
        messages_models.Conversation,
        messages_models.Conversation.sender == sender_id,
    )
    conversations_received = await session.find(
        messages_models.Conversation,
        messages_models.Conversation.receiver == sender_id,
    )
    users_sent = []
    users_received = []
    if conversations_sent:
        conversations_sent_ids = [
            str(conversation.receiver) for conversation in conversations_sent
        ]
        for conversation in conversations_sent:
            receiver = await session.find_one(
                users_models.User,
                users_models.User.id == conversation.receiver,
            )
            user = receiver.dict()
            user["id"] = str(user["id"])
            users_sent.append(user)
    if conversations_received:
        for conversation in conversations_received:
            sender = await session.find_one(
                users_models.User, users_models.User.id == conversation.sender
            )
            user = sender.dict()
            user["id"] = str(user["id"])
            if user["id"] not in conversations_sent_ids:
                users_received.append(user)
    users_sent.extend(users_received)
    users = sorted(users_sent, key=lambda user: user["first_name"])
    results = {"status_code": 200, "result": users}
    return results
