from typing import Optional, List

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
