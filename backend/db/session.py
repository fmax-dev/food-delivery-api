from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.core.config import settings

engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=True
)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db_tables():
    async with engine.begin() as connection:
        from backend import models  # noqa: F401 — register model tables on SQLModel.metadata

        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async with async_session() as session:
        yield session