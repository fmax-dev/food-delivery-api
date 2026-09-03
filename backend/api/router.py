from fastapi import APIRouter

from backend.api.order import order_router
from backend.api.restaurant import restaurant_router

api_router = APIRouter(prefix="/api")
api_router.include_router(restaurant_router)
api_router.include_router(order_router)