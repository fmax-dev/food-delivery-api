from fastapi import APIRouter, HTTPException, Request, status

from backend.api.dependencies import OrderServiceDep, RestaurantServiceDep
from backend.web.template import templates

restaurant_router = APIRouter()


@restaurant_router.get("/restaurants")
async def list_restaurants(
	request: Request,
	service: RestaurantServiceDep,
):
	restaurants = await service.list_restaurants()
	return templates.TemplateResponse(
		request,
		"restaurants/list.html",
		{"restaurants": restaurants},
	)


@restaurant_router.get("/restaurants/{id}")
async def restaurant_detail(
	request: Request,
	id: int,
	service: RestaurantServiceDep,
	order_service: OrderServiceDep,
):
	restaurant = await service.get_restaurant(id)

	if restaurant is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Restaurant not found",
		)

	orders = await order_service.list_for_restaurant(id)
	return templates.TemplateResponse(
		request,
		"restaurants/detail.html",
		{"restaurant": restaurant, "orders": orders},
	)

