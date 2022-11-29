"""The messages models module"""

from bson import (
    ObjectId,
)
from datetime import (
    datetime,
)
from enum import (
    Enum,
    IntEnum,
)
from odmantic import (
    Field,
    Model,
)
from typing import (
    List,
    Optional,
)


class MessageStatus(IntEnum):
    """
    The MessageStatus enumeration

    Args:
        Enum (enum.Enum): Enum base class.
    """

    READ = 0
    NOT_READ = 1


class MessageType(str, Enum):
    """
    The MessageType enumeration

    Args:
        Enum (enum.Enum): Enum base class.
    """

    TEXT = "text"
    MEDIA = "media"


class Message(Model):
    """
    The Message model

    Args:
        Model (odmantic.Model): Odmantic base model.
    """

    content: str
    message_type: str = Field(index=True, default=MessageType.TEXT.value)
    status: int = Field(index=True, default=MessageStatus.NOT_READ.value)
    media: Optional[str] = Field(index=True)
    creation_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    modified_date: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Conversation(Model):
    """
    The Conversation model

    Args:
        Model (odmantic.Model): Odmantic base model.
    """

    sender: ObjectId = Field(index=True)
    receiver: ObjectId = Field(index=True)
    messages: List[ObjectId] = []
    creation_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    modified_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
