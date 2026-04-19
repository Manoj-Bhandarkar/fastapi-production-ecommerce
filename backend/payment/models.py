from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, ForeignKey, Enum
from src.db.base import Base

from enum import Enum as PyEnum


class PaymentStatusEnum(str, PyEnum):
  pending = "pending"
  success = "success"
  failed = "failed"
  cancelled = "cancelled"

class PaymentGatewayEnum(str, PyEnum):
  mock = "mock"
  razorpay = "razorpay"

class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[PaymentStatusEnum] = mapped_column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.pending, nullable=False)
    payment_gateway: Mapped[PaymentGatewayEnum] = mapped_column(Enum(PaymentGatewayEnum), default=PaymentGatewayEnum.mock, nullable=False)
    is_paid: Mapped[bool] = mapped_column(Boolean, default=False)
