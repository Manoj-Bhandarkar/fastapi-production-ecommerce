from fastapi import HTTPException, status
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.cart.models import CartItem
from src.product.models import Product
from src.shipping.models import ShippingAddress, ShippingStatusEnum
from src.order.models import Order, OrderItem, OrderStatusEnum
from src.payment.schemas import PaymentCreate


async def checkout(
    session: AsyncSession, user_id: int, payment_data: PaymentCreate
) -> Order:
    # Fetch all cart items for the user, locking rows for update (to prevent race conditions)
    stmt = (
        select(CartItem)
        .where(CartItem.user_id == user_id)
        .options(selectinload(CartItem.product))
        .with_for_update()
    )

    result = await session.execute(stmt)
    cart_items = result.scalars().all()

    # If no items found, cart is empty → checkout not possible
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
        )
