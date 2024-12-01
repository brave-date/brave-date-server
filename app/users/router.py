"""The users router module"""

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
from odmantic.session import (
    AIOSession,
)
import os
from pinatapy import (
    PinataPy,
)
from tempfile import (
    NamedTemporaryFile,
)
from typing import (
    Any,
    Dict,
    Union,
)

from app.config import (
    settings,
)
from app.users import (
    crud as users_crud,
    schemas as users_schemas,
)
from app.utils import (
    dependencies,
    jwt,
)

router = APIRouter(prefix="/api/v1")

pinata = PinataPy(settings().PINATA_API_KEY, settings().PINATA_API_SECRET)


@router.get("/user/profile", response_model=users_schemas.UserSchema)
async def get_user_profile(
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
) -> Dict[str, Any]:
    """
    Get user profile info given a token provided in a request header.
    """
    results = {
        "token": None,
        "user": users_schemas.UserObjectSchema(
            **jsonable_encoder(current_user)
        ),
        "status_code": 200,
        "message": "Welcome to Brave Date.",
    }
    return results


@router.get("/user/all", response_model=users_schemas.UsersSchema)
async def get_all_users(
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Fetch all users available in the app and not in the matches list.
    """
    return await users_crud.get_users(current_user.id, session)


@router.get("/user/logout")
async def logout(
    token: str = Depends(jwt.get_token_user),
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Log out a user from the app by removing the access token from the list.
    """
    await users_crud.remove_token(current_user.id, token, session)
    return {"status": 200, "message": "Good Bye!"}


@router.put("/user/profile-image")
async def upload_profile_image(
    file: UploadFile = File(...),
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    Upload an image to Pinata Cloud.
    """
    try:
        file_bytes = file.file.read()
        temp = NamedTemporaryFile(delete=False)
        with temp as temp_file:
            temp_file.write(file_bytes)
        result = pinata.pin_file_to_ipfs(temp.name)
        image_url = f"https://ipfs.io/ipfs/{result['IpfsHash']}/{temp.name.split('/')[-1]}"  # noqa: E231
        await users_crud.update_profile_picture(
            email=current_user.email, file_name=image_url, session=session
        )
        return {
            "status_code": 200,
            "message": "Profile picture has been uploaded successfully!",
        }

    except Exception:
        return {"status_code": 400, "message": "Something went wrong!"}

    finally:
        os.remove(temp.name)


@router.put("/user/reset-password")
async def reset_user_password(
    request: users_schemas.ResetPassword,
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    An endpoint for resetting users passwords.
    """
    result = await users_crud.update_user_password(
        request, current_user.email, session
    )
    return result


@router.put("/user/profile")
async def update_personal_information(
    personal_info: users_schemas.PersonalInfo,
    current_user: users_schemas.UserObjectSchema = Depends(
        jwt.get_current_active_user
    ),
    session: AIOSession = Depends(dependencies.get_db_transactional_session),
) -> Dict[str, Any]:
    """
    An endpoint for updating users personel info.
    """
    await users_crud.update_user_info(personal_info, current_user, session)
    return {
        "status_code": 200,
        "message": "Your personal information has been updated successfully!",
    }
