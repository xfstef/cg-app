from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app.core.models import StatusMessage
from app.users.crud import UsersCRUD
from app.users.dependencies import get_users_crud
from app.users.schemas import (UserPatch, UserRead, UserRegister)

router = APIRouter()


@router.post(
    "",
    response_model=UserRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_user(
        data: UserRegister,
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
        users: UsersCRUD = Depends(get_users_crud)
):
    user = await users.patch(user_id=user_id, data=data)

    return user


@router.delete(
    "/{user_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_user(
        user_id: str,
        users: UsersCRUD = Depends(get_users_crud)
):
    deleted = await users.delete(user_id=user_id)

    return {"status": deleted, "message": "The user has been deleted!"}
