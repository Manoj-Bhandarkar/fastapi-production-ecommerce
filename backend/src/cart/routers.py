from fastapi import APIRouter, Depends
from src.account.deps import get_current_user
from src.account.models import User
from src.db.config import SessionDep
from src.cart.schemas import CartItemCreate, CartItemOut, CartSummary
from src.cart.services import add_to_cart, list_user_cart

router = APIRouter()


@router.post("/add", response_model=CartItemOut)
async def add_item_to_cart(
    session: SessionDep, item: CartItemCreate, user: User = Depends(get_current_user)
):
    return await add_to_cart(session, item, user.id)


@router.get("", response_model=CartSummary)
async def list_user_cart_item(
    session: SessionDep, user: User = Depends(get_current_user)
):
    return await list_user_cart(session, user.id)
