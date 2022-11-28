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


class Match(Model):
    """
    The Match model

    Args:
        Model (odmantic.Model): Odmantic base model.
    """

    user: ObjectId
    matches: List[ObjectId] = []
    creation_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    modified_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
