from uuid import UUID

from sqlalchemy.orm import RelationshipProperty
from sqlmodel import Field, Relationship

from app.core.models import (TimestampModel, UUIDModel)

prefix = "pst"


class PublicPost(
    TimestampModel,
    UUIDModel,
    table=True
):
    __tablename__ = f"{prefix}_posts"

    title: str = Field(
        nullable=False,
        max_length=100
    )

    text: str = Field(
        nullable=False,
        max_length=1000
    )

    author_user_id: UUID = Field(
        default=None,
        foreign_key="usr_users.uuid",
        primary_key=True,
        nullable=False
    )

    author: "User" = Relationship(
        sa_relationship=RelationshipProperty(
            "User",
            back_populates="posts",
            uselist=False
        )
    )
