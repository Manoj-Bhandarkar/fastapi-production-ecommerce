from pydantic import BaseModel


class ShippingAddressBase(BaseModel):
    name: str
    address_line1: str
    address_line2: str | None = None
    city: str
    state: str
    pin_code: str
    country: str


class ShippingAddressCreate(ShippingAddressBase):
    pass


class ShippingAddressOut(ShippingAddressBase):
    id: int
    user_id: int
    model_config = {"from_attributes": True}
