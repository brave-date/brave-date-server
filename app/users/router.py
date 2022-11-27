from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    responses,
)
from fastapi.encoders import (
    jsonable_encoder,
)
from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
)
from odmantic.session import (
    AIOSession,
)
from typing import (
    Any,
    Dict,
)

from app.users import (
    crud as user_crud,
    models as users_models,
    schemas as users_schemas,
)
from app.utils import (
    dependencies,
    jwt,
)

router = APIRouter(prefix="/api/v1")


@router.get("/user/profile", response_model=users_schemas.UserSchema)
async def get_user_profile(
    currentUser: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
) -> Dict[str, Any]:
    """
    Get user profile info given a token provided in a request header.
    """
    results = {
        "token": None,
        "user": users_schemas.UserObjectSchema(
            **jsonable_encoder(currentUser)
        ),
        "status_code": 200,
        "message": "Welcome to Brave Date.",
    }
    return results


@router.get("/user/logout")
async def logout(
    token: str = Depends(jwt.get_token_user),
    currentUser: users_models.User = Depends(jwt.get_current_active_user),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    await user_crud.remove_token(currentUser.id, token, session)
    return {"status": 200, "message": "Good Bye!"}
