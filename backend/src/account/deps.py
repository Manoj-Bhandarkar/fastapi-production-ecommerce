from fastapi import HTTPException, status, Request
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
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or Expired Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalide Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    stmt = select(User).where(User.id == int(user_id))
    user = await session.scalar(stmt)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalide Token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
