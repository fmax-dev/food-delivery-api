import asyncio

from fastapi import APIRouter, HTTPException, Query, status

from backend.api.dependencies import OrderServiceDep
from backend.models.order import OrderStatus
from backend.schemas.order import OrderCreate, OrderRead, OrderUpdate

order_router = APIRouter(
    prefix="/order",
    tags=["Order"]
)


# Get latest orders
@order_router.get("/latest", response_model=OrderRead)
async def get_latest_order(service: OrderServiceDep):
    """Retrieve the latest order"""

    latest_orders = await service.get_latest()

    if latest_orders is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No orders yet!"
        )

    return latest_orders


# Fetch multiple orders at the same time
@order_router.get("/bulk", response_model=list[OrderRead])
async def get_several_orders(
    service: OrderServiceDep,
    ids: list[int] = Query(...),
):
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(service.get_order_in_session(order_id))
            for order_id in ids
        ]

    orders = []
    for task in tasks:
        order = task.result()
        if order is not None:
            orders.append(order)

    return orders


# Get a given order
@order_router.get("/{id}", response_model=OrderRead)
async def get_order(id: int, service: OrderServiceDep):
    """Retrieve an order based on a given ID"""

    order = await service.get_order(id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found!"
        )

    return order


# Get Orders with optional params
@order_router.get("", response_model=list[OrderRead])
async def list_orders(
service: OrderServiceDep,
status_filter: OrderStatus | None = Query(default=None, alias="status"),  # noqa: B008
restaurant_id: int | None = None,
min_price: float | None = None,
max_price: float | None = None,
limit: int = 50,
offset: int = 0
):
    """Retrieve a list of orders with optional filters, search terms, and pagination"""

    order = await service.list_orders(
        status=status_filter,
        restaurant_id=restaurant_id,
        min_price=min_price,
        max_price=max_price,
        limit=limit,
        offset=offset
    )

    return order


# Create an Order
@order_router.post("",
status_code=status.HTTP_201_CREATED)
async def create_order(
service: OrderServiceDep,
order_body: OrderCreate,
) -> OrderRead:
    """Create an order with the given data"""

    return await service.add_order(order_body)


# Partially Update an Order
@order_router.patch("/{id}", response_model=OrderRead)
async def update_order(
id: int, 
service: OrderServiceDep,
body: OrderUpdate
):
    """Partially update an order"""

    update_data = body.model_dump(exclude_none=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided to update the order"
        )

    return await service.update_order(id, update_data)


# Delete a given order
@order_router.delete("/{id}")
async def delete_order(id: int, service: OrderServiceDep):
    """Delete a given order"""

    await service.delete_order(id)

    return {"detail": "Order deleted successfully!"}