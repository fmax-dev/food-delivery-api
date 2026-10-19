from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.models.order import Order, OrderStatus
from backend.models.restaurant import Restaurant
from backend.schemas.order import OrderCreate
from backend.db.session import async_session


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Get an Order
    async def get_order(self, id: int) -> Order | None:
        return await self.session.get(Order, id)

    # Get order in new session
    async def get_order_in_session(self, id: int) -> Order | None:
        async with async_session() as session:
            return await session.get(Order, id)

    # latest Order
    async def get_latest(self) -> Order | None:
        # Querying orders, sort by timestamps descending, and get the absolute top row
        query = (
            select(Order).order_by(Order.created_at.desc()).limit(1)
        )

        # Executing the async query
        result = await self.session.exec(query)

        return result.first()

    # List Orders
    async def list_orders(self, 
    status: OrderStatus | None = None,
    restaurant_id: int | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    limit: int = 50,
    offset: int = 0
    ) -> list[Order]:
        statement = select(Order)

        if status is not None:
            statement = statement.where(Order.status == status)

        if restaurant_id is not None:
            statement = statement.where(Order.restaurant_id == restaurant_id)

        if min_price is not None:
            statement = statement.where(Order.total_price >= min_price)

        if max_price is not None:
            statement = statement.where(Order.total_price <= max_price)

        statement = statement.limit(limit).offset(offset)

        result = await self.session.exec(statement)

        return result.all()

    # List Orders for Restaurant
    async def list_for_restaurant(self,
    restaurant_id: int,
    status=None,
    min_price=None,
    max_price=None,
    limit=50,
    offset=0
    ) -> list[Order]:
        return await self.list_orders(
            restaurant_id=restaurant_id,
            status=status,
            min_price=min_price,
            max_price=max_price,
            limit=limit,
            offset=offset
        )

    # Create an Order
    async def add_order(self, order_create: OrderCreate) -> Order:
        # Checking if Restaurant exists
        restaurant = await self.session.get(Restaurant, order_create.restaurant_id)

        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found!"
            )

        # Converting Pydantic data into an unpacked dictionary for the SQLAlchemy model
        new_order = Order(
            **order_create.model_dump(),
            status = OrderStatus.placed,
            estimated_delivery = datetime.now() + timedelta(minutes=35)  # noqa: DTZ005
        )

        # Adding the new object to the tracking session
        self.session.add(new_order)

        # Commiting and refreshing the DB
        await self.session.commit()
        await self.session.refresh(new_order)

        return new_order

    # Updating Order
    async def update_order(self, id: int, update_data: dict) -> Order:
        # Checking if the Order exist
        updated_order = await self.session.get(Order, id)

        if not updated_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No such order exists!"
            )

        # If exists, then check if it's cancelled
        if updated_order.status == OrderStatus.cancelled:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot update a cancelled order!"
            )

        # If all check passed, then we update order
        updated_order.sqlmodel_update(update_data)

        # Commit and refresh DB
        await self.session.commit()
        await self.session.refresh(updated_order)

        return updated_order

    # Delete Order
    async def delete_order(self, id: int) -> None:
        # Checking the status of the order
        deleted_order = await self.session.get(Order, id)

        if not deleted_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cannot delete an order that doesn't exist!"
            )

        if deleted_order.status == OrderStatus.out_for_delivery:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete an order that's already out for delivery!"
            )

        # Otherwise, we delete and commit
        await self.session.delete(deleted_order)
        await self.session.commit()

