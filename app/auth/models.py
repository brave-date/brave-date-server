from bson import (
    ObjectId,
)
from datetime import (
    datetime,
)
from odmantic import (
    Field,
    Model,
    Reference,
)
from typing import (
    List,
    Optional,
)


class AccessToken(Model):
    """
    AccessToken model

    Args:
        mixins.TimestampMixin (odmantic.Model): Common model for Timestamps data.
    """

    user: ObjectId
    tokens: List[str] = []
    creation_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    modified_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
