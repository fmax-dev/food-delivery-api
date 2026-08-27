from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.db.session import get_session
from backend.services.order import OrderService
from backend.services.restaurant import RestaurantService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_restaurant_service(session: SessionDep) -> RestaurantService:
    return RestaurantService(session)

RestaurantServiceDep = Annotated[RestaurantService, Depends(get_restaurant_service)]


def get_order_service(session: SessionDep) -> OrderService:
    return OrderService(session)

OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]