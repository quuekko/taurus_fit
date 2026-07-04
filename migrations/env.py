import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 1. Імпортуємо наш конфіг та базову модель
from src.config import settings
from src.database.models.base import Base
# Обов'язково імпортуємо ВСІ моделі, щоб Alembic "побачив" їх у Base.metadata
from src.database.models.user import User
from src.database.models.workout import WorkoutLog
from src.database.models.nutrition import NutritionLog

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Вказуємо метадані наших моделей
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    # Динамічно передаємо URL з Pydantic налаштувань
    url = settings.database_url_async
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    # Динамічно підставляємо конфігурацію підключення
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = settings.database_url_async

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())