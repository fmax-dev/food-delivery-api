from datetime import datetime

from pydantic import BaseModel, Field

from backend.models.order import OrderStatus


class OrderBase(BaseModel):
    restaurant_id: int
    customer_name: str
    items_summary: str = Field(max_length=100)
    total_price: float = Field(ge=0, le=500)
    delivery_address: str


class OrderRead(OrderBase):
    id: int
    status: OrderStatus = Field(default=OrderStatus.placed)
    estimated_delivery: datetime
    created_at: datetime = Field(default_factory=datetime.now)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: OrderStatus | None = Field(default=None)
    delivery_address: str | None = Field(default=None)