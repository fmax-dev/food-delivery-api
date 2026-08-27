from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.models.order import Order
from backend.models.restaurant import Restaurant
from backend.schemas.restaurant import RestaurantCreate


class RestaurantService:
    def __init__(self, session: AsyncSession):
        self.session = session

    # Get a Restaurant
    async def get_restaurant(self, id: int) -> Restaurant | None:
        return await self.session.get(Restaurant, id)

    # List a Restaurant
    async def list_restaurants(self,
    cuisine_type: str | None = None,
    is_open: bool | None = None,
    name_search: str | None = None,
    limit: int = 50,
    offset: int = 0
    ) -> list[Restaurant]:

        statement = select(Restaurant)

        if cuisine_type is not None:
            statement = statement.where(Restaurant.cuisine_type == cuisine_type)

        if is_open is not None:
            statement = statement.where(Restaurant.is_open == is_open)

        if name_search is not None:
            statement = statement.where(Restaurant.name.ilike(f"%{name_search}%"))

        statement = statement.limit(limit).offset(offset)

        result = await self.session.exec(statement)
        return result.all()

    # Add a Restaurant
    async def add_restaurant(self, restaurant_create: RestaurantCreate
    ) -> Restaurant:
        # Convert Pydantic data into an unpacked dictionary for the SQLAlchemy model
        new_restaurant = Restaurant(**restaurant_create.model_dump())

        # Adding the new object to the tracking session
        self.session.add(new_restaurant)
        # Committing it to the DB
        await self.session.commit()
        # Refreshing to load the db-generated fileds
        await self.session.refresh(new_restaurant)

        return new_restaurant

    # Update a Restaurant
    async def update_restaurant(self, 
    id: int,
    update_data: dict
    ) -> Restaurant:
        # Checking if the Restaurant exists
        restaurant = await self.session.get(Restaurant, id)

        # Raise an HTTPExceptio if doesn't exist
        if restaurant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cannot update a Restaurant that doesn't exist!"
            )

        # Otherwise we proceed
        restaurant.sqlmodel_update(update_data)

        # Commit and refresh db
        await self.session.commit()
        await self.session.refresh(restaurant)

        return restaurant

    # Delete a Restaurant
    async def delete_restaurant(self, id: int) -> None:
        # Checking if Restaurant exists
        restaurant = await self.session.get(Restaurant, id)

        # Raise an HTTPException if doesn't exist
        if not restaurant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cannot delete a Restaurant that doesn't exist!"
            )

        # If exists, we check if it has orders
        orders_stmt = select(Order).where(Order.restaurant_id == id).limit(1)
        existing_order = (await self.session.exec(orders_stmt)).first()

        if existing_order is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete a Restaurant with existing orders"
            )

        # Deleting the Restaurant now
        await self.session.delete(restaurant)
        await self.session.commit()
