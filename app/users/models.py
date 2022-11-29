"""The users models module"""

from datetime import (
    datetime,
)
from enum import (
    Enum,
    IntEnum,
)
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
    """
    The ChatStatus enumeration

    Args:
        Enum (enum.Enum): Base enum class.
    """

    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    DONT_DISTURB = "don't disturb"


class UserStatus(IntEnum):
    """
    The UserStatus enumeration

    Args:
        Enum (enum.Enum): Base enum class.
    """

    ACTIVE = 1
    DISABLED = 0


class UserRole(str, Enum):
    """
    The UserRole enumeration

    Args:
        Enum (enum.Enum): Base enum class.
    """

    REGULAR = "regular"
    ADMIN = "admin"


class UserGender(str, Enum):
    """
    The UserGender enumeration

    Args:
        Enum (enum.Enum): Base enum class.
    """

    MAN = "man"
    WOMAN = "woman"
    OTHER = "other"


class GenderInterests(str, Enum):
    """
    The GenderInterests enumeration

    Args:
        Enum (enum.Enum): Base enum class.
    """

    MAN = "man"
    WOMAN = "woman"
    EVERYONE = "everyone"


class DisplayGender(IntEnum):
    """
    The DisplayGender enumeration

    Args:
        Enum (enum.Enum): Base enum class.
    """

    YES = 1
    NO = 0


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
    chat_status: Optional[ChatStatus] = Field(default=ChatStatus.ONLINE.value)
    user_status: Optional[UserStatus] = Field(default=UserStatus.ACTIVE.value)
    user_role: Optional[UserRole] = Field(default=UserRole.REGULAR.value)
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
