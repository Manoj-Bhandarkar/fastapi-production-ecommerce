from sqlalchemy.ext.asyncio import AsyncSession
from src.shipping.schemas import ShippingAddressCreate, ShippingAddressOut
from src.shipping.models import ShippingAddress


async def create_shipping_address(
    session: AsyncSession,
    user_id: int,
    data: ShippingAddressCreate
) -> ShippingAddressOut:
  address = ShippingAddress(user_id=user_id, **data.model_dump())
  session.add(address)
  await session.commit()
  await session.refresh(address)
  return address
