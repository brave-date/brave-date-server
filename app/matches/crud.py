"""Matches Crud module."""

from bson import (
    ObjectId,
)
from datetime import (
    datetime,
)
from fastapi.encoders import (
    jsonable_encoder,
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
)
from app.matches import (
    models as matches_models,
)
from app.users import (
    models as users_models,
)


async def add_new_match(
    match: EmailStr, user_id: ObjectId, session: AIOSession
) -> Dict[str, Any]:
    """
    A method to insert a user id into a user matches list.

    Args:
        match (pydantic.EmailStr) : A given user email to add into the matches list.
        user_id (bson.ObjectId) : A given id of an authenticated user.
        session (odmantic.session.AIOSession) : odmantic session object.

    Returns:
        Dict[str, Any]: A Response dict.
    """
    match_user = await auth_crud.find_existed_user(match, session)
    if not match_user:
        return {
            "status_code": 400,
            "message": "You can't add a non existing user to"
            " your matches list!",
        }
    if match_user.id == user_id:
        return {
            "status_code": 400,
            "message": "You can't add yourself to your matches list!",
        }
    match = await session.find_one(
        matches_models.Match, matches_models.Match.user == user_id
    )
    if not match:
        match = matches_models.Match(
            user=user_id,
            matches=[
                match_user.id,
            ],
        )
    else:
        matches = match.matches
        if match_user.id in matches:
            return {
                "status_code": 400,
                "message": f"{match_user.first_name} already exist in your"
                " matches list!",
            }
        matches.extend(
            [
                match_user.id,
            ]
        )
        match.update(
            {
                "user": user_id,
                "matches": matches,
                "modified_date": datetime.utcnow(),
            }
        )
    await session.save(match)
    results = {
        "status_code": 201,
        "message": f"{match_user.first_name} has been added to your matches"
        " list!",
    }
    return results


async def get_user_matches(
    user_id: ObjectId, session: AIOSession
) -> Dict[str, Any]:
    """
    A method to fetch all user matches info.

    Args:
        user_id (bson.ObjectId) : A given id of an authenticated user.
        session (odmantic.session.AIOSession) : odmantic session object.

    Returns:
        Dict[str, Any]: A User model instance
    """
    match = await session.find_one(
        matches_models.Match, matches_models.Match.user == user_id
    )
    if match:
        matches = match.matches
        user_list_ids = []
        for match_user_id in matches:
            match = await session.find_one(
                matches_models.Match,
                matches_models.Match.user == match_user_id,
            )
            if match and user_id in match.matches:
                user_list_ids.append(match_user_id)
        users = await session.find(
            users_models.User, users_models.User.id.in_(user_list_ids)
        )
        return {"status_code": 200, "result": jsonable_encoder(users)}
    return {"status_code": 400, "message": "You don't have matches!"}
