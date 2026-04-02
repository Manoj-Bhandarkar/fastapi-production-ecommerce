from fastapi import APIRouter, Depends, HTTPException, status
from src.account.deps import require_admin
from src.account.models import User
from src.db.config import SessionDep
from src.product.schemas import CategoryCreate, CategoryOut
from src.product.services import create_category, get_all_category

router = APIRouter()

@router.post("/", response_model=CategoryOut)
async def category_create(session:SessionDep, category:CategoryCreate, admin_user=Depends(require_admin)):
    return await create_category(session, category)

@router.get("/", response_model=list[CategoryOut])
async def list_categories(session:SessionDep):
    return await get_all_category(session)