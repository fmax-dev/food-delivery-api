from fastapi import APIRouter, Request

from backend.api.dependencies import OrderServiceDep, RestaurantServiceDep
from backend.web.template import templates

order_router = APIRouter()


@order_router.get("/orders")
async def list_orders(
    request: Request,
    service: OrderServiceDep,
    restaurant_service: RestaurantServiceDep,
):
    orders = await service.list_orders()
    restaurants = await restaurant_service.list_restaurants(limit=1000)
    restaurant_names = {restaurant.id: restaurant.name for restaurant in restaurants}
    return templates.TemplateResponse(
        request,
        "orders/list.html",
        {"orders": orders, "restaurant_names": restaurant_names},
    )