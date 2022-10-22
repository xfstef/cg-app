from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app import settings
from app.auth.models import TokenPayload
from app.users.crud import UsersCRUD
from app.users.dependencies import get_users_crud
from app.users.models import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_prefix}/auth/access-token"
)


async def get_current_user(
        users: UsersCRUD = Depends(get_users_crud),
        token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.auth_secret_key,
            algorithms=[settings.auth_algorithm]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user hasn't been authorized!"
        )

    user = await users.get_auth(user_id=token_data.sub)
    return user
