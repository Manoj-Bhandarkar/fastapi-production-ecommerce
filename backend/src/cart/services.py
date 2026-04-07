from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.cart.models import CartItem
from src.cart.schemas import CartItemCreate, CartItemOut
from src.product.models import Product

async def add_to_cart(
    session: AsyncSession,
    data: CartItemCreate,
    user_id: int
):
  product = await session.get(Product, data.product_id)
  if not product:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
  if product.stock_quantity < data.quantity:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient stock")
  
  stmt = select(CartItem).where(CartItem.user_id == user_id, CartItem.product_id == data.product_id)
  result = await session.execute(stmt)
  item = result.scalar_one_or_none()

  if item:
    item.quantity += data.quantity
    item.price = product.price
  else:
    item = CartItem(
      user_id = user_id,
      product_id = data.product_id,
      quantity = data.quantity,
      price = product.price
    )
    session.add(item)
  await session.commit()
  await session.refresh(item)

  return CartItemOut(
    id = item.id,
    user_id = item.user_id,
    product_id=item.product_id,
    product_title=product.title,
    quantity=item.quantity,
    price=product.price,
    total=round(product.price * item.quantity, 2)
  )  
