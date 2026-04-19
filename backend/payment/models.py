from enum import Enum as PyEnum

class PaymentStatusEnum(str, PyEnum):
  pending = "pending"
  success = "success"
  failed = "failed"
  cancelled = "cancelled"

class PaymentGatewayEnum(str, PyEnum):
  mock = "mock"
  razorpay = "razorpay"