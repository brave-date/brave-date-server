"""Matches router module."""

from fastapi import (
    APIRouter,
    Depends,
)
from odmantic.session import (
    AIOSession,
)
from typing import (
    Any,
    Dict,
    Union,
)

from app.auth.schemas import (
    ResponseSchema,
)
from app.matches import (
    crud as matches_crud,
)
from app.matches.schemas import (
    AddMatch,
    GetAllMatchesResults,
)
from app.users import (
    schemas as users_schemas,
)
from app.utils import (
    dependencies,
    jwt,
)

router = APIRouter(prefix="/api/v1")


@router.post(
    "/matches",
    response_model=ResponseSchema,
    status_code=201,
    name="matches:add-match",
    responses={
        201: {
            "model": ResponseSchema,
            "description": "Return a message that indicates a new user"
            "has been added to the matches list.",
        },
        400: {
            "model": ResponseSchema,
            "description": "Return this response in case of non existing user"
            " or an already existed one in the match list.",
        },
    },
)
async def add_match(
    match: AddMatch,
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Add new user to an authenticated user matches list.
    """
    results = await matches_crud.add_new_match(
        match.match, current_user.id, session
    )
    return results


@router.get(
    "/matches",
    response_model=Union[GetAllMatchesResults, ResponseSchema],
    status_code=200,
    name="matches:get-all-user-matches",
    responses={
        200: {
            "model": GetAllMatchesResults,
            "description": "A list of matches for each user.",
        },
        400: {
            "model": ResponseSchema,
            "description": "User not found.",
        },
    },
)
async def get_matches_for_user(
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Get all matches for an authenticated user.
    """
    results = await matches_crud.get_user_matches(current_user.id, session)
    return results
