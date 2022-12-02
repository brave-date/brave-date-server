"""The users crud module"""

from bson import (
    ObjectId,
)
from datetime import (
    datetime,
)
from odmantic.session import (
    AIOSession,
)
from pydantic import (
    EmailStr,
)
from typing import (
    Any,
    Dict,
)

from app.auth import (
    crud as auth_crud,
    models as auth_models,
)
from app.matches import (
    models as matches_models,
)
from app.users import (
    models as users_models,
    schemas as users_schemas,
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
        user_id (bson.ObjectId) : A user id.
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


async def get_users(user_id: ObjectId, session: AIOSession) -> Dict[str, Any]:
    """
    A method for fetching all users registered in the app.

    Args:
        user_id (bson.ObjectId) : A user id.
        session (odmantic.session.AIOSession) : odmantic session object.
    """
    users = await session.find(
        users_models.User, users_models.User.id != user_id
    )
    match = await session.find_one(
        matches_models.Match, matches_models.Match.user == user_id
    )
    matches_ids = []
    if match:
        matches_ids = match.matches
    result = []
    # return users not in matches
    for user in users:
        if user.id not in matches_ids:
            user = user.dict()
            user["id"] = str(user["id"])
            result.append(user)
    return {"status_code": 200, "result": result}


async def update_profile_picture(
    email: EmailStr, file_name: str, session: AIOSession
) -> None:
    """
    A method for fetching all users registered in the app.

    Args:
        email (pydantic.EmailStr) : A user email address.
        file_name (str) : A relative image file path stored on a Deta drive.
        session (odmantic.session.AIOSession) : odmantic session object.
    """
    user = await session.find_one(
        users_models.User, users_models.User.email == email
    )
    user.profile_picture = file_name
    await session.save(user)


async def update_user_password(
    request: users_schemas.ResetPassword, email: EmailStr, session: AIOSession
) -> Dict[str, Any]:
    """
    A method for resetting authenticated user's password.

    Args:
        request (users_schemas.ResetPassword) : A request schema object for reset password.
        email (pydantic.EmailStr) : A user email address.
        session (odmantic.session.AIOSession) : odmantic session object.
    """
    user = await auth_crud.find_existed_user(email, session)
    if not crypt.verify_password(request.old_password, user.password):
        results = {
            "status_code": 400,
            "message": "Your old password is not correct!",
        }
    elif crypt.verify_password(request.new_password, user.password):
        results = {
            "status_code": 400,
            "message": "Your new password can't be your old one!",
        }
    elif not request.new_password == request.confirm_password:
        results = {
            "status_code": 400,
            "message": "Please confirm your new password!",
        }
    else:
        user.update(
            {
                "password": crypt.get_password_hash(request.new_password),
                "modified_date": datetime.utcnow(),
            }
        )
        await session.save(user)
        results = {
            "status_code": 200,
            "message": "Your password has been reseted successfully!",
        }
    return results


async def update_user_info(
    personal_info: users_schemas.PersonalInfo,
    current_user: users_schemas.UserObjectSchema,
    session: AIOSession,
) -> None:
    """
    A method for resetting authenticated user's password.

    Args:
        personal_info (users_schemas.PersonalInfo) : User personal info schema object.
        current_user (users_schemas.UserObjectSchema) : User schema object.
        session (odmantic.session.AIOSession) : odmantic session object.
    """
    current_user.update(
        {
            "first_name": personal_info.first_name,
            "last_name": personal_info.last_name,
            "passion": personal_info.passion,
            "phone_number": personal_info.passion,
            "modified_date": datetime.utcnow(),
        }
    )
    await session.save(current_user)
