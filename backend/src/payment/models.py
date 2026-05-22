from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Enum, String
from src.account.models import User
from src.order.models import Order
from src.db.base import Base
from decimal import Decimal
from sqlalchemy import Numeric
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
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[PaymentStatusEnum] = mapped_column(
        Enum(PaymentStatusEnum),
        default=PaymentStatusEnum.pending,
        nullable=False,
        index=True,
    )
    payment_gateway: Mapped[PaymentGatewayEnum] = mapped_column(
        Enum(PaymentGatewayEnum), default=PaymentGatewayEnum.mock, nullable=False
    )

    pg_order_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pg_payment_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True, index=True
    )
    pg_signature: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="payment",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="payments",
    )
