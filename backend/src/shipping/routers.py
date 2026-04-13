from fastapi import APIRouter, Depends
from src.db.config import SessionDep
from src.account.models import User
from src.account.deps import get_current_user
from src.shipping.schemas import ShippingAddressOut, ShippingAddressCreate
from src.shipping.services import create_shipping_address, list_user_shipping_addresses


router = APIRouter()

@router.post("/addresses", response_model=ShippingAddressOut)
async def shipping_address_create(
  session: SessionDep,
  data: ShippingAddressCreate,
  user: User = Depends(get_current_user)
):
  return await create_shipping_address(session, user.id, data)

@router.get("/addresses", response_model=list[ShippingAddressOut])
async def shipping_addresses_user_list(
  session: SessionDep,
  user: User = Depends(get_current_user)
):
  return await list_user_shipping_addresses(session, user.id)
