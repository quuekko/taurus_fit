from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.nutrition import NutritionLog
from src.database.repositories.base import BaseRepository

class NutritionRepository(BaseRepository[NutritionLog]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=NutritionLog, session=session)