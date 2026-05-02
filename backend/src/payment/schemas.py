from pydantic import BaseModel, Field
from typing import Literal

class PaymentCreate(BaseModel):
  amount: int
  shipping_address_id: int
  gateway: Literal["mock", "razorpay"] = Field(default="mock")
  simulate_success: bool | None = None
