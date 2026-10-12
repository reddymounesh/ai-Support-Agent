import enum
from datetime import datetime

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class TicketReason(str, enum.Enum):
    UNCERTAIN_ANSWER = "uncertain_answer"
    INSUFFICIENT_INFO = "insufficient_info"
    CUSTOMER_FRUSTRATED = "customer_frustrated"
    REQUIRES_MANUAL_ACTION = "requires_manual_action"
    OTHER = "other"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id"), nullable=True
    )
    reason: Mapped[TicketReason] = mapped_column(
        SAEnum(TicketReason, name="ticket_reason")
    )
    summary: Mapped[str] = mapped_column(Text)
    status: Mapped[TicketStatus] = mapped_column(
        SAEnum(TicketStatus, name="ticket_status"),
        default=TicketStatus.OPEN,
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)