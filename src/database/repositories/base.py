from typing import Generic, TypeVar, Type, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.database.models.base import Base

# Створюємо змінну типу, яка обов'язково має успадковуватися від Base
ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """Базовий клас для всіх репозиторіїв із стандартними CRUD операціями."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, obj_id: int) -> ModelType | None:
        """Отримує запис за його первинним ключем."""
        query = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def add(self, obj: ModelType) -> ModelType:
        """Додає новий об'єкт в сесію та робить flush для отримання id."""
        self.session.add(obj)
        try:
            await self.session.flush()
            return obj
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def update(self, obj: ModelType) -> ModelType:
        """Зберігає зміни об'єкта (потребує commit на рівні вище)."""
        await self.session.merge(obj)
        await self.session.flush()
        return obj

    async def delete(self, obj: ModelType) -> None:
        """Видаляє об'єкт з бази даних."""
        await self.session.delete(obj)
        await self.session.flush()