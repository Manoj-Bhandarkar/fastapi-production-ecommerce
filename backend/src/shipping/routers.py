from fastapi import APIRouter, Depends
from src.db.config import SessionDep
from src.account.models import User
from src.account.deps import get_current_user
from src.shipping.schemas import ShippingAddressOut, ShippingAddressCreate
from src.shipping.services import create_shipping_address


router = APIRouter()

@router.post("/addresses", response_model=ShippingAddressOut)
async def shipping_address_create(
  session: SessionDep,
  data: ShippingAddressCreate,
  user: User = Depends(get_current_user)
):
  return await create_shipping_address(session, user.id, data)
