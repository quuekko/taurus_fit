from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.user import User
from src.database.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    """Репозиторій для роботи з моделлю User."""

    def __init__(self, session: AsyncSession):
        # Жорстко прив'язуємо модель User до базового класу
        super().__init__(model=User, session=session)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Пошук користувача за його Telegram ID."""
        query = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
        
    async def get_or_create(self, telegram_id: int) -> tuple[User, bool]:
        """
        Повертає користувача, якщо він існує. 
        Якщо ні - створює нового.
        Повертає кортеж (User, is_created).
        """
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            return user, False
            
        new_user = User(telegram_id=telegram_id)
        # add() викликає flush(), тому new_user отримає свій primary key
        new_user = await self.add(new_user)
        return new_user, True