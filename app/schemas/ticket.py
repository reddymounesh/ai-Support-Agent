from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.ticket import TicketReason, TicketStatus


class TicketCreate(BaseModel):
    customer_id: int | None = None
    reason: TicketReason
    summary: str


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int | None
    reason: TicketReason
    summary: str
    status: TicketStatus
    created_at: datetime