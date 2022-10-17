from datetime import datetime, timedelta

from jwt import encode as jwt_encode
from passlib.context import CryptContext

from app import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        subject: str,
        expires_delta: timedelta = None
) -> str:

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.auth_token_expire
        )

    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt_encode(
        payload=to_encode,
        key=settings.auth_secret_key,
        algorithm=settings.auth_algorithm
    )

    return encoded_jwt


def password_validator(values: dict):
    if len(values.get("password_1")) < 10:
        raise ValueError("Password must be at least 10 characters long!")

    if values.get("password_1") != values.get("password_2"):
        raise ValueError("Passwords don't match!")

    symbols = r'~`! @#$%^&*()_-+={[}]|\:;"\'<,>.?/'

    if not any([s in values["password_1"] for s in symbols]):
        raise ValueError(
            f"The password must contain "
            f"at least one of the symbols: {symbols}!"
        )

    if not any([s.isdigit() for s in values["password_1"]]):
        raise ValueError(
            "The password must contain at "
            "least one digit!"
        )

    if not any([s.islower() for s in values["password_1"]]):
        raise ValueError(
            "The password must contain at "
            "least one lowercase letter!"
        )

    if not any([s.isupper() for s in values["password_1"]]):
        raise ValueError(
            "The password must contain at "
            "least one uppercase letter"
        )

    return values
