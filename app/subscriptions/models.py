from uuid import UUID

from sqlmodel import Field, SQLModel

prefix = "sbs"


class Subscription(SQLModel, table=True):
    __tablename__ = f"{prefix}_subscriptions"

    author_user_id: UUID = Field(
        default=None,
        foreign_key="usr_users.uuid",
        primary_key=True,
        nullable=False
    )

    subscriber_user_id: UUID = Field(
        default=None,
        foreign_key="usr_users.uuid",
        primary_key=True,
        nullable=False
    )
