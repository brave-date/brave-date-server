from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import (
    Optional,
)

from app.users.schemas import (
    UserObjectSchema,
)


class MatchCreate(BaseModel):
    user: EmailStr = Field(
        ...,
        example="user1@example.com",
    )
    match: EmailStr = Field(
        ...,
        example="user2@example.com",
    )


class GetAllMatchesResults(BaseModel):
    status_code: int = Field(
        ...,
        example="A response status code. (e.g. 200 on a successful attempt.)",
    )
    result: list[UserObjectSchema]


class AddMatch(BaseModel):
    match: EmailStr = Field(
        ...,
        example="user@example.com",
    )
