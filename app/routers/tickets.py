from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse

router = APIRouter(prefix="/support/tickets", tags=["tickets"])


@router.post("", response_model=TicketResponse, status_code=201)
async def create_ticket(
    ticket_in: TicketCreate,
    db: AsyncSession = Depends(get_db),
) -> Ticket:
    ticket = Ticket(**ticket_in.model_dump())
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db),
) -> Ticket:
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket