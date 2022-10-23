from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel

from app.core.models import UUIDModel


class PostRead(UUIDModel):
    title: str
    text: str
    author_user_id: str | UUID


class PostCreate(SQLModel):
    title: str
    text: str


class PostPatch(SQLModel):
    title: Optional[str]
    text: Optional[str]
