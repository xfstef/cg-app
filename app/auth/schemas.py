from pydantic import BaseModel, root_validator

from app.core.utils import password_validator


class CreatePassword(BaseModel):
    password_1: str
    password_2: str

    @root_validator()
    def passwords(cls, values: dict):  # noqa
        values = password_validator(values=values)
        return values


class ResetPassword(CreatePassword):
    token: str
