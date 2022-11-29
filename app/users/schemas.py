"""The users schemas module"""

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
    Optional,
)


class UserObjectSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for fetching user info.
    """

    id: str = Field(..., example="asdWQdqw123")
    first_name: str = Field(..., example="Your first name.")
    last_name: str = Field(..., example="Your last name.")
    birthday: str = Field(..., example=str(datetime.utcnow().date()))
    gender: str = Field(..., example="man")
    interests: str = Field(..., example="woman")
    display_gender: int = Field(..., example=1)
    passion: List[str] = Field(..., example=["swimming", "cardio"])
    email: EmailStr = Field(..., example="user@test.com")
    profile_picture: str = Field(..., example="A relative URL to Deta Drive.")
    chat_status: Optional[str] = Field(default="online")
    user_status: Optional[int] = Field(default=1)
    user_role: Optional[str] = Field(default="regular")


class UserLoginSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for the login endpoint.
    """

    email: EmailStr = Field(..., example="testing@gmail.com")
    password: str = Field(..., example="A secure password goes here.")


class UserSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for response.
    """

    user: Optional[UserObjectSchema] = Field(
        ...,
        example=UserObjectSchema(
            id="asdWQdqw123",
            first_name="Your first name.",
            last_name="Your last name.",
            birthday=str(datetime.utcnow().date()),
            gender="man",
            interests="woman",
            display_gender=1,
            passion=["swimming", "cardio"],
            email="user@test.com",
            profile_picture="A relative URL to Deta Drive.",
        ),
    )
    token: Optional[dict[str, str]] = Field(
        ..., example="Token value(e.g. 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9')"
    )
    status_code: int = Field(
        ...,
        example="A response status code. (e.g. 200 on a successful attempt.)",
    )
    message: str = Field(
        ...,
        example="A message to indicate whether or not the login was successful!",
    )
