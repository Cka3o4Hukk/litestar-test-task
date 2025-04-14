import pytest_asyncio
from sqlalchemy.ext.asyncio import (AsyncSession,
                                    create_async_engine, async_sessionmaker)
from app.config import settings
from app.models import Base


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Фикстура для создания тестовой сессии базы данных."""
    engine = create_async_engine(settings.database_url, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession
    )
    async with session_factory() as session:
        yield session
    await engine.dispose()
