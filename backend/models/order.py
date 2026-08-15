from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.models.restaurant import Restaurant

class OrderStatus(str, Enum):
    placed = "placed"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(SQLModel, table=True):
    __tablename__ = "order"

    id: int = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    restaurant: Restaurant | None = Relationship(back_populates="orders")
    customer_name: str
    items_summary: str
    total_price: float = Field(ge=0, le=500)
    delivery_address: str
    status: OrderStatus = Field(default=OrderStatus.placed)
    estimated_delivery: datetime
    created_at: datetime = Field(default_factory=datetime.now)
