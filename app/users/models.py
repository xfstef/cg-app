from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.posts.models import PublicPost
from app.core.models import (TimestampModel, UUIDModel)

prefix = "usr"


class UserBase(SQLModel):
    username: str = Field(
        nullable=False,
        max_length=55,
        sa_column_kwargs={"unique": True}
    )

    hashed_password: str

    biography: Optional[str] = Field(
        nullable=True,
        max_length=200,
    )


class User(
    TimestampModel,
    UUIDModel,
    UserBase,
    table=True
):
    __tablename__ = f"{prefix}_users"

    posts: List[PublicPost] = Relationship(
        back_populates="author",
        sa_relationship_kwargs={
            "lazy": "immediate",
            "uselist": True
        }
    )
