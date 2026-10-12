from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ticket import Ticket, TicketReason


async def escalate_to_human(
    db: AsyncSession,
    reason: str,
    summary: str,
    customer_id: int | None = None,
) -> dict:
    """
    Create a support ticket so a human agent can follow up.
    `reason` must be one of the TicketReason enum values.
    """
    try:
        reason_enum = TicketReason(reason)
    except ValueError:
        reason_enum = TicketReason.OTHER

    ticket = Ticket(
        customer_id=customer_id,
        reason=reason_enum,
        summary=summary,
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)

    return {
        "escalated": True,
        "ticket_id": ticket.id,
        "message": (
            "A support ticket has been created and a human agent will "
            "follow up with you shortly."
        ),
    }