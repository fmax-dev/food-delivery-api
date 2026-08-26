from fastapi import HTTPException, status
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.models.order import Order


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Get an Order
    async def get_orders(self, id: int) -> Order | None:
        return await self.session.get(Order, id)

    # latest Order
    async def get_latest(self) -> Order | None:
        pass