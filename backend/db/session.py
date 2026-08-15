from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from backend.core.config import settings

engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True
)


async def create_db_tables():
    async with engine.begin() as connection:
        from backend.models import Order, Restaurant
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session