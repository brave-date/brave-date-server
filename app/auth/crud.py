"""Auth Crud module."""

from bson import (
    ObjectId,
)
from datetime import (
    datetime,
    timedelta,
)
from fastapi.encoders import (
    jsonable_encoder,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
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
    Optional,
)

from app.auth import (
    models as auth_models,
    schemas as auth_schemas,
)
from app.users import (
    models as users_models,
    schemas as users_schemas,
)
from app.utils import (
    crypt,
    jwt,
)


async def create_user(
    user: auth_schemas.UserCreate, session: AIOSession
) -> users_models.User:
    """
    A method to insert a user into the users table.

    Args:
        user (auth_schemas.UserCreate) : A user schema object that contains all info about a user.
        session (odmantic.session.AIOSession) : odmantic session object.

    Returns:
        users_models.User: A User model instance
    """
    user = users_models.User(**user.dict())
    await session.save(user)
    return user


async def find_existed_user(
    email: str, session: AIOSession
) -> users_models.User:
    """
    A method to fetch a user info given an email.

    Args:
        email (EmailStr) : A given user email.
        session (odmantic.session.AIOSession) : Odmantic session object.

    Returns:
        users_models.User: The current user object.
    """
    user = await session.find_one(
        users_models.User, users_models.User.email == email
    )
    return user


async def find_existed_user_id(
    user_id: str, session: AIOSession
) -> Optional[users_models.User]:
    """
    A method to fetch a user info given an id.

    Args:
        user_id (str) : A given user id.
        session (odmantic.session.AIOSession) : Odmantic session object.

    Returns:
        users_models.User: The current user object.
    """
    user = await session.find_one(
        users_models.User, users_models.User.id == ObjectId(user_id)
    )
    if user:
        return users_schemas.UserObjectSchema(**jsonable_encoder(user))
    return None


async def login_user(
    form_data: OAuth2PasswordRequestForm, session: AIOSession
) -> Dict[str, Any]:
    """
    A method to fetch and return serialized user info upon logging in.

    Args:
        form_data (OAuth2PasswordRequestForm) : OAuth2 request form.
        session (odmantic.session.AIOSession) : Odmantic session object.

    Returns:
        Dict[str, Any]: a dict object that contains info about a given user.
    """
    user_obj = await find_existed_user(form_data.username, session)
    if not user_obj:
        return {"status_code": 404, "message": "User not found!"}
    user = auth_schemas.UserLoginSchema(
        email=user_obj.email, password=user_obj.password
    )
    is_valid = crypt.verify_password(form_data.password, user.password)
    if not is_valid:
        return {"status_code": 401, "message": "Invalid Credentials!"}

    access_token_expires = timedelta(minutes=60)
    access_token = await jwt.create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires,
    )

    token = await session.find_one(
        auth_models.AccessToken, auth_models.AccessToken.user == user_obj.id
    )
    if not token:
        token = auth_models.AccessToken(
            user=user_obj.id,
            tokens=[
                access_token["access_token"],
            ],
        )
    else:
        tokens = token.tokens
        tokens.extend(
            [
                access_token["access_token"],
            ]
        )
        token.update(
            {
                "user": user_obj.id,
                "tokens": tokens,
                "modified_date": datetime.utcnow(),
            }
        )
    await session.save(token)

    return access_token


async def register_user(
    user: auth_schemas.UserCreate, session: AIOSession
) -> Dict[str, Any]:
    """
    A method to fetch and return serialized user info upon registering a new account.

    Args:
        user (auth_schemas.UserCreate) : A auth_schemas.UserCreate schema object.
        session (odmantic.session.AIOSession) : Odmantic session object.

    Returns:
        Dict[str, Any]: a dict object that contains info about a given user.
    """
    fetched_user = await find_existed_user(user.email, session)
    if fetched_user:
        return {"status_code": 400, "message": "User already signed up!"}

    # Create new user
    user.password = crypt.get_password_hash(user.password)
    await create_user(user, session)
    user = await find_existed_user(user.email, session)
    access_token_expires = timedelta(minutes=60)
    access_token = await jwt.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    # Serialize user object.
    results = {
        "user": users_schemas.UserObjectSchema(**jsonable_encoder(user)),
        "token": access_token,
        "status_code": 201,
        "message": "Welcome. Start matchin'!",
    }
    return results


async def find_existed_token(
    email: EmailStr, token: str, session: AIOSession
) -> Optional[str]:
    """
    A method for finding a token in a token list.

    Args:
        email (pydantic.EmailStr) : An email address of an authenticated user.
        token (str) : A token value.
        session (odmantic.session.AIOSession) : odmantic session object.
    """
    user = await find_existed_user(email, session)
    token_obj = await session.find_one(
        auth_models.AccessToken, auth_models.AccessToken.user == user.id
    )
    try:
        tokens = token_obj.tokens
        if token in tokens:
            return token
    except Exception:
        ...
    return None
