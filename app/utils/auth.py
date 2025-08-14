from datetime import timedelta
from passlib.context import CryptContext
from ..configs.settings import settings
from fastapi_jwt import JwtAccessBearer


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_security = JwtAccessBearer(
    settings.SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_TIMEDELTA)),
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def generate_access_token(subject: dict) -> str:
    return access_security.create_access_token(subject)
