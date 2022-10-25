from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import select, update, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.exceptions import HTTP403UsernameExists
from app.core.utils import get_password_hash
from app.users.models import User
from app.users.schemas import (UserCreate, UserPatch)


class UsersCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate, commit: bool = True) -> User:
        exists = await self.find_by_username(username=data.username)
        if exists:
            raise HTTP403UsernameExists()

        data.hashed_password = get_password_hash(password=data.hashed_password.password_1)
        user = User(**data.dict())
        self.session.add(user)

        if commit:
            await self.session.commit()
        else:
            await self.session.flush()

        await self.session.refresh(user)

        return user

    async def get_auth(self, user_id: str | UUID) -> User:
        statement = select(
            User.uuid,
            User.hashed_password,
            User.username
        ).where(
            User.uuid == user_id
        )
        results = await self.session.execute(statement=statement)
        user = results.one_or_none()

        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )

        return User.parse_obj(user)

    async def get(self, user_id: str | UUID) -> User:
        where_clause = [User.uuid == user_id]

        statement = select(
            User
        ).where(
            *where_clause
        )
        results = await self.session.execute(statement=statement)
        user: User | None = results.scalar_one_or_none()

        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )

        return user

    async def patch(
            self,
            user_id: str | UUID,
            data: UserPatch
    ) -> User:
        user = await self.get(user_id=user_id)

        values = data.dict(exclude_unset=True)

        for key, value in values.items():
            setattr(user, key, value)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def patch_password(
            self,
            user_id: str | UUID,
            password: str
    ) -> bool:
        hashed_password = get_password_hash(password=password)
        statement = update(
            User
        ).where(
            User.uuid == user_id
        ).values(
            {"hashed_password": hashed_password}
        )
        await self.session.execute(statement=statement)
        await self.session.commit()

        return True

    async def delete(self, user_id: str) -> bool:
        where_clause = [User.uuid == user_id]

        statement = delete(
            User
        ).where(
            *where_clause
        )
        await self.session.execute(statement=statement)
        await self.session.commit()

        return True

    async def find_by_username(
            self,
            username: str
    ) -> User:
        statement = select(
            User
        ).where(
            User.username == username
        )

        results = await self.session.execute(statement)
        user = results.scalars().one_or_none()

        return user
