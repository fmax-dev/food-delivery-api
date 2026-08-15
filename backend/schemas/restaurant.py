from datetime import datetime

from pydantic import BaseModel, Field


class RestaurantBase(BaseModel):
    name: str
    cuisine_type: str
    is_open: bool = Field(default=True)
    rating: float | None = Field(ge=0, le=5)


class RestaurantRead(RestaurantBase):
    id: int
    created_at: datetime


class Restaurant(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: str | None = Field(default=None)
    cuisine_type: str | None = Field(default=None)
    is_open: bool | None = Field(default=None)
    rating: float | None = Field(default=None, ge=0, le=5)

