from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from decouple import config
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from src.account.models import User, RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_ACCESS_TOKEN_TIME_MIN = config("JWT_ACCESS_TOKEN_TIME_MIN")
JWT_ALGORITHM = config("JWT_ALGORITHM")
JWT_SECRET_KEY = config("JWT_SECRET_KEY")
JWT_REFRESH_TOKEN_TIME_DAY = config("JWT_REFRESH_TOKEN_TIME_DAY")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify_password(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=JWT_ACCESS_TOKEN_TIME_MIN)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
