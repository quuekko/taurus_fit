from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.config import settings

import src.database.models

# Створюємо асинхронний двіжок. echo=True корисний на етапі розробки (виводить SQL у консоль)
engine = create_async_engine(
    settings.database_url_async,
    echo=True,
    future=True,
    pool_pre_ping=True  # Перевіряє "живе" підключення перед використанням
)

# Фабрика асинхронних сесій
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Запобігає неочікуваному завантаженню атрибутів після коміту
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Генератор для отримання сесії БД (Dependency Injection / Middleware pattern)"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()