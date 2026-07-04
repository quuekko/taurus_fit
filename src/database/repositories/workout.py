from datetime import date, timedelta
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.workout import WorkoutLog
from src.database.repositories.base import BaseRepository

class WorkoutRepository(BaseRepository[WorkoutLog]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=WorkoutLog, session=session)

    async def get_recent_workouts(self, user_id: int, days: int = 30) -> list[WorkoutLog]:
        """Отримує історію тренувань користувача за вказану кількість днів."""
        since_date = date.today() - timedelta(days=days)
        
        query = (
            select(WorkoutLog)
            .where(
                WorkoutLog.user_id == user_id,
                WorkoutLog.date >= since_date
            )
            .order_by(desc(WorkoutLog.date))  # Нові тренування спочатку
        )
        
        result = await self.session.execute(query)
        return list(result.scalars().all())