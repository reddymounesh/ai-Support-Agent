from datetime import datetime

from pydantic import BaseModel,ConfigDict

from app.models.order import OrderStatus

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    customer_id: int
    product_name: str
    status: OrderStatus
    order_date: datetime
    expected_delivery: datetime | None