from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from backend.models.order import Order


class Restaurant(SQLModel, table=True):
    __tablename__ = "restaurant"

    id: int = Field(default=None, primary_key=True)
    name: str
    cuisine_type: str
    is_open: bool = Field(default=True)
    rating: float | None = Field(default=None, ge=0, le=5)
    created_at: datetime = Field(default_factory=datetime.now)
    orders: list[Order] = Relationship(back_populates="restaurant")
