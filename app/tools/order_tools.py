from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order


async def get_order_status(db: AsyncSession, order_id: int) -> dict:
    """
    Look up a single order by ID and return its status info.
    Returns a plain dict (not an ORM object) — this is deliberately the
    ONLY shape of data the LLM will ever see for this order.
    """
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if order is None:
        return {"found": False, "error": f"No order found with id {order_id}"}

    return {
        "found": True,
        "order_id": order.id,
        "product_name": order.product_name,
        "status": order.status.value,
        "order_date": order.order_date.isoformat(),
        "expected_delivery": (
            order.expected_delivery.isoformat() if order.expected_delivery else None
        ),
    }


async def get_customer_orders(db: AsyncSession, customer_id: int) -> dict:
    """
    Look up all orders belonging to a customer.
    """
    result = await db.execute(select(Order).where(Order.customer_id == customer_id))
    orders = result.scalars().all()

    if not orders:
        return {"found": False, "error": f"No orders found for customer {customer_id}"}

    return {
        "found": True,
        "orders": [
            {
                "order_id": o.id,
                "product_name": o.product_name,
                "status": o.status.value,
            }
            for o in orders
        ],
    }