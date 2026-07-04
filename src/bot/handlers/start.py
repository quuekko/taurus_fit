from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from src.database.repositories.user import UserRepository

# Створюємо роутер для організації хендлерів
router = Router(name="start_router")

@router.message(CommandStart())
async def cmd_start(message: Message, user_repo: UserRepository):
    """Обробник команди /start. Реєструє користувача в БД."""
    
    # Використовуємо наш репозиторій для перевірки або створення юзера
    user, is_created = await user_repo.get_or_create(telegram_id=message.from_user.id)
    
    if is_created:
        await message.answer(
            "Вітаю! Я твій <b>AI Smart Trainer</b>. Бачу, ти тут вперше. 💪\n\n"
            "Напиши мені свої параметри (зріст, вагу) та ціль, щоб ми почали!"
        )
    else:
        await message.answer(
            "З поверненням! Готовий залогувати нове тренування чи прийом їжі?"
        )