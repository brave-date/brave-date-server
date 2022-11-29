"""The messages schemas module."""

from datetime import (
    datetime,
)
from pydantic import (
    BaseModel,
    Field,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)


class MessageCreate(BaseModel):
    """
    A Pydantic class that defines the message schema to create a message object.
    """

    receiver: str = Field(..., example="KV1QiLCJhbGciOiJIUzI1NiJ")
    content: str = Field(..., example="Hello World!")
    message_type: str = Field(..., example="text")
    media: Optional[str] = Field(..., example="")


class GetAllMessageResult(BaseModel):
    """
    A Pydantic class that defines the message schema to fetch messages info.
    """

    sender: str = Field(..., example="KV1QiLCJhbGciOiJIUzI1NiJ")
    receiver: str = Field(..., example="KdasdfsaV1QiLCJhbGcizI1w")
    messages: List[str] = Field(..., example="['Hello there!', ]")
    creation_date: datetime = Field(..., example=datetime.utcnow())
    modified_date: datetime = Field(..., example=datetime.utcnow())


class GetAllMessageResults(BaseModel):
    """
    A Pydantic class that defines the message schema to fetch all messages results.
    """

    status_code: int = Field(..., example=200)
    result: List[Dict[str, Any]]
