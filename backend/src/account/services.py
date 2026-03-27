from src.account.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from fastapi import HTTPException, status
from src.account.schemas import UserCreate, UserLogin
from src.account.utils import hash_password, verify_password

async def create_user(session: AsyncSession, user: UserCreate):
    stmt = Select(User).where(User.email == user.email)
    result = await session.scalar(stmt)

    if result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    new_user = User(email=user.email, hashed_password=hash_password(user.password))

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


async def authenticate_user(session: AsyncSession, user_login: UserLogin):
    stmt = Select(User).where(User.email == user_login.email)
    result = await session.scalers(stmt)
    user = result.first()

    if not user or not verify_password(user_login.password, user.hashed_password):
        return None
    
    return user