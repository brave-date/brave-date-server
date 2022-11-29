"""Auth model module."""

from bson import (
    ObjectId,
)
from datetime import (
    datetime,
)
from odmantic import (
    Field,
    Model,
)
from typing import (
    List,
    Optional,
)


class AccessToken(Model):
    """
    The AccessToken model

    Args:
        Model (odmantic.Model): Base odmantic model.
    """

    user: ObjectId
    tokens: List[str] = []
    creation_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    modified_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
