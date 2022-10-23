from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.subscriptions.crud import SubscriptionsCRUD


async def get_subscriptions_crud(
        session: AsyncSession = Depends(get_async_session)
) -> SubscriptionsCRUD:
    return SubscriptionsCRUD(session=session)
