import asyncio
from datetime import datetime, timedelta

from app.database import Base, AsyncSessionLocal, engine
from app.models.customer import Customer
from app.models.order import Order, OrderStatus


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_data() -> None:
    async with AsyncSessionLocal() as session:
        customer1 = Customer(name="Asha Rao", email="asha.rao@example.com")
        customer2 = Customer(name="Vikram Shah", email="vikram.shah@example.com")

        session.add_all([customer1, customer2])
        await session.flush()  # assigns IDs without committing yet

        order1 = Order(
            customer_id=customer1.id,
            product_name="Wireless Headphones",
            status=OrderStatus.SHIPPED,
            expected_delivery=datetime.now() + timedelta(days=2),
        )
        order2 = Order(
            customer_id=customer1.id,
            product_name="Laptop Stand",
            status=OrderStatus.DELIVERED,
        )
        order3 = Order(
            customer_id=customer2.id,
            product_name="Mechanical Keyboard",
            status=OrderStatus.PENDING,
            expected_delivery=datetime.now() + timedelta(days=5),
        )

        session.add_all([order1, order2, order3])
        await session.commit()

    print("Seed data inserted.")


async def main() -> None:
    await create_tables()
    await seed_data()


if __name__ == "__main__":
    asyncio.run(main())