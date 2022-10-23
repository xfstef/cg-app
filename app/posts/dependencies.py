from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.posts.crud import PostsCRUD


async def get_posts_crud(
        session: AsyncSession = Depends(get_async_session)
) -> PostsCRUD:
    return PostsCRUD(session=session)
