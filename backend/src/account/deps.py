from fastapi import Depends, HTTPException, status, Request
from sqlalchemy import select
from src.db.config import SessionDep
from src.account.models import User
from src.account.utils import decode_token


async def get_current_user(session: SessionDep, request: Request):
    # is_authenticated give name also
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Access Token",
        )
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired Token",
        )
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token Payload",
        )
    stmt = select(User).where(User.id == int(user_id))
    user = await session.scalar(stmt)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Not Found",
        )
    return user


async def require_admin(user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive account")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email verification required")

    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return user
