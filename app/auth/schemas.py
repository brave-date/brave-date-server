"""Auth Schemas module."""

from datetime import (
    datetime,
)
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from typing import (
    Optional,
)

from app.users import (
    schemas as users_schemas,
)


class UserSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for registration.
    """

    user: Optional[users_schemas.UserObjectSchema] = Field(
        ...,
        example=users_schemas.UserObjectSchema(
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


class UserLoginSchema(BaseModel):
    """
    A Pydantic class that defines the user schema for logging in.
    """

    email: EmailStr = Field(..., example="Your email address to log in.")
    password: str = Field(..., example="A secure password goes here.")


class UserCreate(BaseModel):
    """
    A Pydantic class that defines the user schema for sign up.
    """

    first_name: str = Field(..., example="Your first name.")
    last_name: str = Field(..., example="Your last name.")
    birthday: str = Field(..., example=str(datetime.utcnow().date()))
    gender: str = Field(..., example="man")
    interests: str = Field(..., example="woman")
    display_gender: int = Field(..., example=1)
    passion: str = Field(..., example="swimming,cardio")
    email: EmailStr = Field(..., example="user@test.com")
    password: str = Field(..., example="A secure password goes here.")
    profile_picture: str = Field(..., example="A relative URL to Deta Drive.")


class Token(BaseModel):
    """
    A Pydantic class that defines the Token schema.
    """

    access_token: str = Field(
        ..., example="Token value(e.g. 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9')"
    )


class TokenData(BaseModel):
    """
    A Pydantic class that defines a Token schema to return the email address.
    """

    email: Optional[str] = Field(..., example="Your email address.")


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
