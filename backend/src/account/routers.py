from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from src.db.config import SessionDep
from src.account.schemas import UserCreate, UserOut, UserLogin
from src.account.services import create_user, authenticate_user
from src.account.utils import create_tokens

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register(session: SessionDep, user: UserCreate):
    return await create_user(session, user)


@router.post("/login")
async def login(session: SessionDep, user_login: UserLogin):
    user = await authenticate_user(session, user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    tokens = await create_tokens(session, user)
    response = JSONResponse(content={"message":"Login Successful"})
    response.set_cookie(
        "access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60*60*24*1
    )
    response.set_cookie(
        "refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60*60*24*7
    )
    return response