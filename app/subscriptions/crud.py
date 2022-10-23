from typing import List
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import HTTP404, HTTP403SubscriptionExists, HTTP403SubscriptionsLimit, HTTP409
from app.subscriptions.models import Subscription
from app.users.crud import UsersCRUD


class SubscriptionsCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UsersCRUD(session)

    async def add_subscription(
            self,
            username: str,
            user_id: str | UUID
    ) -> Subscription:
        creator = await self.users.find_by_username(username=username)
        if not creator:
            raise HTTP404()

        if creator.uuid == user_id:
            raise HTTP409()

        exists = await self.get(author_user_id=creator.uuid, subscriber_user_id=user_id)
        if exists:
            raise HTTP403SubscriptionExists()

        all_subs = await self.get_all_subscriptions(subscriber_user_id=user_id)
        if len(all_subs) > 99:
            raise HTTP403SubscriptionsLimit()

        subscription = Subscription(author_user_id=creator.uuid, subscriber_user_id=user_id)
        self.session.add(subscription)

        await self.session.commit()

        await self.session.refresh(subscription)

        return subscription

    async def get(self, author_user_id: str | UUID, subscriber_user_id: str | UUID) -> Subscription:
        where_clause = [
            Subscription.author_user_id == author_user_id,
            Subscription.subscriber_user_id == subscriber_user_id
        ]

        statement = select(
            Subscription
        ).where(
            *where_clause
        )
        results = await self.session.execute(statement=statement)
        subscription: Subscription | None = results.scalar_one_or_none()

        return subscription

    async def get_all_subscriptions(self, subscriber_user_id: str | UUID) -> List[Subscription]:
        where_clause = [
            Subscription.subscriber_user_id == subscriber_user_id
        ]

        statement = select(
            Subscription
        ).where(
            *where_clause
        )
        results = await self.session.execute(statement=statement)
        subscriptions = results.scalars().all()

        return subscriptions

    async def remove_subscription(
            self,
            username: str,
            user_id: str | UUID
    ) -> bool:
        creator = await self.users.find_by_username(username=username)
        if not creator:
            raise HTTP404()

        if creator.uuid == user_id:
            raise HTTP409()

        where_clause = [
            Subscription.author_user_id == creator.uuid,
            Subscription.subscriber_user_id == user_id
        ]

        statement = delete(
            Subscription
        ).where(
            *where_clause
        )
        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
