from fastapi import APIRouter

from backend.web.order import order_router
from backend.web.restaurant import restaurant_router

web_router = APIRouter()
web_router.include_router(restaurant_router)
web_router.include_router(order_router)
