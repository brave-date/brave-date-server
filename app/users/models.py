from datetime import (
    datetime,
)
from enum import Enum
from odmantic import (
    Field,
    Index,
    Model,
)
from pydantic import (
    EmailStr,
)
from typing import (
    List,
    Optional,
)


class ChatStatus(str, Enum):
    online = "online"
    offline = "offline"
    busy = "busy"
    dont_disturb = "don't disturb"


class UserStatus(int, Enum):
    active = 1
    disabled = 0


class UserRole(str, Enum):
    regular = "regular"
    admin = "admin"


class UserGender(str, Enum):
    man = "man"
    woman = "woman"
    other = "other"


class GenderInterests(str, Enum):
    man = "man"
    woman = "woman"
    everyone = "everyone"


class DisplayGender(int, Enum):
    yes = 1
    no = 0


class User(Model):
    """
    The User model

    Args:
        Model (odmantic.Model): Odmantic base model.
    """

    first_name: str = Field(index=True)
    last_name: str = Field(...)
    birthday: str = Field(...)
    gender: UserGender = Field(...)
    interests: GenderInterests = Field(...)
    display_gender: DisplayGender = Field(...)
    passion: List[str] = []
    email: EmailStr = Field(index=True)
    password: str = Field(index=True)
    profile_picture: str = Field(...)
    phone_number: Optional[str]
    chat_status: Optional[ChatStatus] = Field(default=ChatStatus.online.value)
    user_status: Optional[UserStatus] = Field(default=UserStatus.active.value)
    user_role: Optional[UserRole] = Field(default=UserRole.regular.value)
    creation_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    modified_date: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        """
        The User Config class.
        """

        @staticmethod
        def indexes() -> Index:
            """
            Indexes definition.

            Yields:
                Index: return a compound index on the email and password fields,
            """
            yield Index(User.email, User.password, name="email_password_index")


__all__ = [
    "ChatStatus",
    "UserStatus",
    "UserRole",
    "User",
]
