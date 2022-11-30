"""The match schemas module"""

from datetime import (
    datetime,
)
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import (
    List,
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
    result: List[UserObjectSchema] = Field(
        ...,
        example=[
            UserObjectSchema(
                id="asdWQdqw123",
                first_name="Your first name.",
                last_name="Your last name.",
                birthday=str(datetime.utcnow().date()),
                gender="man",
                interests="woman",
                display_gender=1,
                passion="swimming,cardio",
                email="user@test.com",
                profile_picture="A relative URL to Deta Drive.",
            ),
        ],
    )


class AddMatch(BaseModel):
    """
    A Pydantic class that defines a match schema for the match endpoint param.
    """

    match: EmailStr = Field(
        ...,
        example="user@example.com",
    )


class ResponseSchema(BaseModel):
    """
    A Pydantic class that defines a Response schema object.
    """

    status_code: int = Field(
        ...,
        example=400,
    )
    message: str = Field(
        ...,
        example="A message to indicate that the request was not successful!",
    )
