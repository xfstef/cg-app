from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

from app import User
from app.auth.dependencies import get_current_user
from app.core.models import StatusMessage
from app.users.crud import UsersCRUD
from app.users.dependencies import get_users_crud
from app.users.schemas import (UserPatch, UserRead, UserCreate)

router = APIRouter()


@router.post(
    "",
    response_model=UserRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_user(
        data: UserCreate,
        users: UsersCRUD = Depends(get_users_crud)
):
    user = await users.create(data=data)

    return user


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    status_code=http_status.HTTP_200_OK
)
async def patch_user(
        user_id: str,
        data: UserPatch,
        users: UsersCRUD = Depends(get_users_crud),
        user: User = Depends(get_current_user)  # noqa
):
    if user_id != str(user.uuid):
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Unauthorised attempt to modify the user!"
        )

    user = await users.patch(user_id=user_id, data=data)

    return user


@router.delete(
    "/{user_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_user(
        user_id: str,
        users: UsersCRUD = Depends(get_users_crud),
        user: User = Depends(get_current_user)  # noqa
):
    if user_id != str(user.uuid):
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Unauthorised attempt to modify the user!"
        )

    deleted = await users.delete(user_id=user_id)

    return {"status": deleted, "message": "The user has been deleted!"}
