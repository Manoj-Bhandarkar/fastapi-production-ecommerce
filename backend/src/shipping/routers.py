from fastapi import APIRouter, Depends
from src.db.config import SessionDep
from src.account.models import User
from src.account.deps import get_current_user
from src.shipping.schemas import ShippingAddressOut, ShippingAddressCreate, ShippingAddressUpdate
from src.shipping.services import (
    create_shipping_address,
    get_user_shipping_address_by_address_id,
    list_user_shipping_addresses,
    update_user_shipping_address_by_address_id,
)


router = APIRouter()


@router.post("/addresses", response_model=ShippingAddressOut)
async def shipping_address_create(
    session: SessionDep,
    data: ShippingAddressCreate,
    user: User = Depends(get_current_user),
):
    return await create_shipping_address(session, user.id, data)


@router.get("/addresses", response_model=list[ShippingAddressOut])
async def shipping_addresses_user_list(
    session: SessionDep, user: User = Depends(get_current_user)
):
    return await list_user_shipping_addresses(session, user.id)


@router.get("/addresses/{address_id}", response_model=ShippingAddressOut)
async def shipping_address_user_by_address_id(
    session: SessionDep, address_id: int, user: User = Depends(get_current_user)
):
    return await get_user_shipping_address_by_address_id(session, address_id, user.id)

@router.patch("/addresses/{address_id}", response_model=ShippingAddressOut)
async def user_shipping_address_update_by_address_id(
  session: SessionDep,
  address_id: int,
  data: ShippingAddressUpdate,
  user: User = Depends(get_current_user)
):
  return await update_user_shipping_address_by_address_id(session, address_id, user.id, data)
