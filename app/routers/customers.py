from fastapi import APIRouter, HTTPException ,Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession 

from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import  CustomerResponse

router = APIRouter(prefix="/customers",tags=["customers"])


@router.get("/{customer_id}",response_model=CustomerResponse)
async def get_customer(
    customer_id: int, db: AsyncSession = Depends(get_db),)->Customer:
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
