from typing import Optional
from pydantic import root_validator

from app.core.utils import password_validator
from app.core.models import UUIDModel
from app.users.models import UserBase


class UserRegister(UserBase):
    password_1: str
    password_2: str

    @root_validator()
    def passwords(cls, values: dict):  # noqa: class method
        values = password_validator(values=values)

        return values


class UserRead(UserBase, UUIDModel):
    username: str
    biography: Optional[str]


class UserCreate(UserBase):
    hashed_password: str


class UserPatch(UserBase):
    username: str
    biography: Optional[str]
