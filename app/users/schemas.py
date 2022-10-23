from typing import Optional, List
from pydantic import root_validator

from app.core.utils import password_validator
from app.core.models import UUIDModel
from app.users.models import UserBase
from app import PublicPost


class UserRead(UUIDModel):
    username: str
    biography: Optional[str]
    posts: Optional[List[PublicPost]]


class UserCreate(UserBase):
    hashed_password: str


class UserPatch(UUIDModel):
    username: str
    biography: Optional[str]
