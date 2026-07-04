from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from src.database.repositories.workout import WorkoutRepository
from src.database.repositories.nutrition import NutritionRepository

from src.database.connection import AsyncSessionLocal
from src.database.repositories.user import UserRepository

class DbSessionMiddleware(BaseMiddleware):
    """Middleware для створення сесії БД та репозиторіїв на кожен запит."""
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Відкриваємо асинхронну сесію
        async with AsyncSessionLocal() as session:
            # Ініціалізуємо репозиторії та передаємо їх у контекст data
            data["session"] = session
            data["user_repo"] = UserRepository(session)
            data["workout_repo"] = WorkoutRepository(session)
            data["nutrition_repo"] = NutritionRepository(session)
            
            try:
                # Передаємо управління наступному middleware або обробнику
                result = await handler(event, data)
                
                # Якщо обробник відпрацював без помилок, комітимо зміни
                await session.commit()
                return result
            except Exception as e:
                # Якщо сталася помилка (наприклад, збій ШІ), відкочуємо зміни
                await session.rollback()
                raise e