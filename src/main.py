import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config import settings
from src.bot.middlewares.db import DbSessionMiddleware
from src.bot.handlers.start import router as start_router
from src.bot.handlers.messages import router as messages_router

# Налаштування базового логування для консолі
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting AI Smart Trainer Bot...")
    
    # Ініціалізуємо бота (ParseMode.HTML дозволяє використовувати теги <b>, <i> тощо)
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Ініціалізуємо диспетчер
    dp = Dispatcher()
    
    # Реєструємо Middleware на рівні повідомлень
    dp.message.middleware(DbSessionMiddleware())
    
    # Підключаємо наші роутери з обробниками
    dp.include_router(start_router)
    dp.include_router(messages_router)
    
    # Запускаємо polling. drop_pending_updates ігнорує повідомлення,
    # які користувачі могли написати, поки бот був вимкнений.
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        # Щоб уникнути помилок з ProactorEventLoop на Windows
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped gracefully.")