import enum
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    product_name: Mapped[str] = mapped_column(String(200))
    status: Mapped[OrderStatus] = mapped_column(
        SAEnum(OrderStatus, name="order_status"),
        default=OrderStatus.PENDING,
    )
    order_date: Mapped[datetime] = mapped_column(default=datetime.now)
    expected_delivery: Mapped[datetime | None] = mapped_column(nullable=True)

    customer: Mapped["Customer"] = relationship(back_populates="orders")