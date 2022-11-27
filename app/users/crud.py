from bson import (
    ObjectId,
)
from datetime import (
    datetime,
)
from odmantic.session import (
    AIOSession,
)

from app.auth import (
    models as auth_models,
)
from app.utils import (
    crypt,
)


async def remove_token(
    user_id: ObjectId, token: str, session: AIOSession
) -> None:
    """
    A method for removing a token from a token list.

    Args:
        token (str) : A token value.
        session (odmantic.session.AIOSession) : odmantic session object.
    """
    token_obj = await session.find_one(
        auth_models.AccessToken, auth_models.AccessToken.user == user_id
    )
    tokens = token_obj.tokens
    if token in tokens:
        tokens.remove(token)
        token_obj.update(
            {
                "user": user_id,
                "tokens": tokens,
                "modified_date": datetime.utcnow(),
            }
        )
        await session.save(token_obj)
