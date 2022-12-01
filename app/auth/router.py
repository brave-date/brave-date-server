"""Auth router module."""

from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from odmantic.session import (
    AIOSession,
)
from typing import (
    Any,
    Dict,
    Union,
)

from app.auth import (
    crud as auth_crud,
    schemas as auth_schemas,
)
from app.utils import (
    dependencies,
)

router = APIRouter(prefix="/api/v1")


@router.post(
    "/auth/login",
    response_model=Union[auth_schemas.Token, auth_schemas.ResponseSchema],
    status_code=200,
    name="auth:login",
    responses={
        201: {
            "model": auth_schemas.Token,
            "description": "A response object contains a token object for a user"
            " e.g. Token value: {access_token: 'abcdefg12345token', token_type: 'Bearer'}",
        },
        400: {
            "model": auth_schemas.ResponseSchema,
            "description": "A response object indicates that a user"
            " was not found!",
        },
        401: {
            "model": auth_schemas.ResponseSchema,
            "description": "A response object indicates that invalid"
            " credentials were provided!",
        },
    },
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Authenticate a user.
    """
    access_token = await auth_crud.login_user(form_data, session)
    return access_token


@router.post(
    "/auth/register",
    name="auth:register",
    response_model=Union[auth_schemas.UserSchema, auth_schemas.ResponseSchema],
    responses={
        201: {
            "model": auth_schemas.UserCreate,
            "description": "A response object that contains a welcome message"
            " on a successfull login!",
        },
        400: {
            "model": auth_schemas.ResponseSchema,
            "description": "A response object to indicate that a user has already signed up"
            " using this email!",
        },
    },
)
async def register(
    user: auth_schemas.UserCreate,
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    register a new user.
    """
    results = await auth_crud.register_user(user, session)
    return results
