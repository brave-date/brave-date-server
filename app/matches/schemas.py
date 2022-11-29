"""The match schemas module"""

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from app.users.schemas import (
    UserObjectSchema,
)


class MatchCreate(BaseModel):
    """
    A Pydantic class that defines a match schema to add a user into a match list.
    """

    user: EmailStr = Field(
        ...,
        example="user1@example.com",
    )
    match: EmailStr = Field(
        ...,
        example="user2@example.com",
    )


class GetAllMatchesResults(BaseModel):
    """
    A Pydantic class that defines a match schema to return users info list.
    """

    status_code: int = Field(
        ...,
        example="A response status code. (e.g. 200 on a successful attempt.)",
    )
    result: list[UserObjectSchema]


class AddMatch(BaseModel):
    """
    A Pydantic class that defines a match schema for the match endpoint param.
    """

    match: EmailStr = Field(
        ...,
        example="user@example.com",
    )
