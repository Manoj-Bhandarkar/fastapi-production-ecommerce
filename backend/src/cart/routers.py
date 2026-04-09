from fastapi import APIRouter, Depends
from src.account.deps import get_current_user
from src.account.models import User
from src.db.config import SessionDep
from src.cart.schemas import CartItemCreate, CartItemOut, CartSummary
from src.cart.services import add_to_cart, change_cart_item_quantity_by_product, list_user_cart

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

@router.patch("/increase/{product_id}", response_model=CartItemOut)
async def increase_quantity_by_product(
  session: SessionDep,
  product_id: int,
  user: User = Depends(get_current_user)
):
  return await change_cart_item_quantity_by_product(session, product_id, user.id, delta=1)
