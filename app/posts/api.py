from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as http_status

from app import User
from app.auth.dependencies import get_current_user
from app.core.models import StatusMessage
from app.posts.crud import PostsCRUD
from app.posts.dependencies import get_posts_crud
from app.posts.schemas import (PostPatch, PostRead, PostCreate)

router = APIRouter()


@router.post(
    "",
    response_model=PostRead,
    status_code=http_status.HTTP_201_CREATED
)
async def create_post(
        data: PostCreate,
        posts: PostsCRUD = Depends(get_posts_crud),
        user: User = Depends(get_current_user)  # noqa
):
    post = await posts.create(user_id=user.uuid, data=data)

    return post


@router.patch(
    "/{post_id}",
    response_model=PostRead,
    status_code=http_status.HTTP_200_OK
)
async def patch_post(
        post_id: str,
        data: PostPatch,
        posts: PostsCRUD = Depends(get_posts_crud),
        user: User = Depends(get_current_user)  # noqa
):
    post = await posts.get(post_id=post_id)
    if post.author_user_id != user.uuid:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Unauthorised attempt to modify the post!"
        )

    post = await posts.patch(post_id=post_id, data=data)

    return post


@router.delete(
    "/{post_id}",
    response_model=StatusMessage,
    status_code=http_status.HTTP_200_OK,
)
async def delete_post(
        post_id: str,
        posts: PostsCRUD = Depends(get_posts_crud),
        user: User = Depends(get_current_user)  # noqa
):
    post = await posts.get(post_id=post_id)
    if post.author_user_id != user.uuid:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Unauthorised attempt to delete a post!"
        )

    deleted = await posts.delete(post_id=post_id)

    return {"status": deleted, "message": "The post has been deleted!"}
