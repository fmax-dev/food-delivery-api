from fastapi import APIRouter, HTTPException, Query, status

from backend.api.dependencies import OrderServiceDep, RestaurantServiceDep
from backend.models.order import OrderStatus
from backend.schemas.order import OrderRead
from backend.schemas.restaurant import (
    RestaurantCreate,
    RestaurantRead,
    RestaurantUpdate,
)

restaurant_router = APIRouter(
    prefix="/restaurant",
    tags=["Restaurant"]
)

# List all Restaurants with optional params
@restaurant_router.get("", 
response_model=list[RestaurantRead], 
status_code=status.HTTP_200_OK)
async def list_restaurants(
service: RestaurantServiceDep,
cuisine_type: str | None = None,
name_search: str | None = None,
is_open: bool | None = None,
limit: int = 50,
offset: int = 0
):
    """Retrieve a list of restaurants using optional filters, search terms and pagination"""

    restaurant = await service.list_restaurants(
        cuisine_type=cuisine_type,
        name_search=name_search,
        is_open=is_open,
        limit=limit,
        offset=offset
    )

    return restaurant


# List a given restaurant
@restaurant_router.get("/{id}", response_model=RestaurantRead)
async def get_restaurant(
service: RestaurantServiceDep, 
id: int
):
    """Retrieve a specific restaurant with a given id"""

    restaurant = await service.get_restaurant(id=id)

    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant doesn't exist!"
        )

    return restaurant


# Create a Restaurant
@restaurant_router.post("",
status_code=status.HTTP_201_CREATED)
async def create_restaurant(
service: RestaurantServiceDep,        
restaurant_body: RestaurantCreate
) -> RestaurantRead:
    """Create a restaurant with the given body"""

    return await service.add_restaurant(restaurant_body)


# Partially Update a Restaurant
@restaurant_router.patch("/{id}", response_model=RestaurantRead)
async def update_restaurant(
id: int,        
service: RestaurantServiceDep, 
body: RestaurantUpdate
):
    """Update a restaurant with partial data"""

    updated_resto = body.model_dump(exclude_none=True)

    if not updated_resto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update Restaurant!"
        )

    restaurant = await service.update_restaurant(id, updated_resto)

    return restaurant


# Delete a Restaurant
@restaurant_router.delete("/{id}")
async def delete_restaurant(
id: int, 
service: RestaurantServiceDep
):
    """Delete a given restaurant"""

    return await service.delete_restaurant(id)


# List all orders of a restaurant
@restaurant_router.get("/{id}/orders", response_model=list[OrderRead])
async def list_restaurant_orders(
id: int,
service: RestaurantServiceDep,
order_service: OrderServiceDep,
status_filter: OrderStatus | None = Query(default=None, alias="status"),  # noqa: B008
min_price: float | None = None,
max_price: float | None = None,
limit: int = 50,
offset: int = 0        
):
    """Retrieve all orders of a restaurant"""

    # Check if restaurant itself exists!
    restaurant = await service.get_restaurant(id)

    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    return await order_service.list_for_restaurant(
        restaurant_id=id,
        status=status_filter,
        min_price=min_price,
        max_price=max_price,
        limit=limit,
        offset=offset
    )