from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, Enum
from src.db.base import Base
import enum


class OrderStatusEnum(str, enum.Enum):
  pending = "pending"
  confirmed = "confirmed"
  cancelled = "cancelled"

class Order(Base):
  __tablename__ = "orders"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)
  user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  total_price: Mapped[float] = mapped_column(nullable=False)
  status: Mapped[OrderStatusEnum] = mapped_column(Enum(OrderStatusEnum), default=OrderStatusEnum.pending, nullable=False)
  shipping_address_id: Mapped[int] = mapped_column(ForeignKey("shipping_addresses.id"), nullable=False)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

