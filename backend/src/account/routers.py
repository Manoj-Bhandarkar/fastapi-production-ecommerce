from fastapi import APIRouter, HTTPException, status
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
