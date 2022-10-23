from uuid import UUID

from fastapi import status as http_status
from sqlalchemy import select, delete, insert
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import HTTP403PostTitleExists, HTTPException
from app.posts.models import PublicPost
from app.posts.schemas import (PostCreate, PostPatch)


class PostsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            user_id: str | UUID,
            data: PostCreate
    ) -> PublicPost:
        exists = await self.find_by_title(title=data.title, user_id=user_id)
        if exists:
            raise HTTP403PostTitleExists()

        statement = insert(
            PublicPost
        ).values(
            {
                "title": data.title,
                "text": data.text,
                "author_user_id": user_id
            }
        )

        await self.session.execute(statement=statement)
        await self.session.commit()

        post = await self.find_by_title(title=data.title, user_id=user_id)

        return post

    async def get(self, post_id: str | UUID) -> PublicPost:
        where_clause = [PublicPost.uuid == post_id]

        statement = select(
            PublicPost
        ).where(
            *where_clause
        )
        results = await self.session.execute(statement=statement)
        post: PublicPost | None = results.scalar_one_or_none()

        if post is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The post hasn't been found!"
            )

        return post

    async def patch(
            self,
            post_id: str | UUID,
            data: PostPatch
    ) -> PublicPost:
        post = await self.get(post_id=post_id)

        values = data.dict(exclude_unset=True)

        for key, value in values.items():
            setattr(post, key, value)

        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)

        return post

    async def delete(self, post_id: str) -> bool:
        where_clause = [PublicPost.uuid == post_id]

        statement = delete(
            PublicPost
        ).where(
            *where_clause
        )
        await self.session.execute(statement=statement)
        await self.session.commit()

        return True

    async def find_by_title(
            self,
            title: str,
            user_id: str | UUID
    ) -> PublicPost:
        statement = select(
            PublicPost
        ).where(
            PublicPost.title == title,
            PublicPost.author_user_id == user_id
        )

        results = await self.session.execute(statement)
        post = results.scalars().one_or_none()

        return post
