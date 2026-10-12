from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.order import Order
from app.schemas.order import OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db),
) -> Order:
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order