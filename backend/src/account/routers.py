from fastapi import APIRouter
from src.db.config import SessionDep
from src.account.schemas import UserCreate, UserOut
from src.account.services import create_user

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(session: SessionDep, user: UserCreate):
    return await create_user(session, user)