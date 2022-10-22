from fastapi import (APIRouter, Depends, HTTPException, status)
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from app import settings, User
from app.auth.dependencies import get_current_user
from app.auth.models import Token
from app.auth.schemas import ResetPassword
from app.core.models import StatusMessage
from app.core.utils import create_access_token, verify_password
from app.users.crud import UsersCRUD
from app.users.dependencies import get_users_crud

router = APIRouter()


@router.post("/access-token", response_model=Token)
async def get_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        users: UsersCRUD = Depends(get_users_crud)
) -> Token:

    user = await users.find_by_username(username=form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user hasn't been found!"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password!"
        )

    return Token(
        access_token=create_access_token(subject=str(user.uuid)),
        token_type="Bearer"
    )


@router.post("/reset_password", response_model=StatusMessage)
async def reset_password(
        data: ResetPassword,
        users: UsersCRUD = Depends(get_users_crud),
        user: User = Depends(get_current_user)  # noqa
):
    try:
        token_data = jwt.decode(
            token=data.token,
            key=settings.email_secret_key,
            algorithms=[settings.auth_algorithm]
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The credentials are not valid!"
        )

    await users.patch_password(
        user_id=token_data["sub"],
        password=data.password_1
    )

    return {"status": True, "message": "The password has been reset!"}
