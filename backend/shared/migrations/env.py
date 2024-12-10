import asyncio
from logging.config import fileConfig
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool
from alembic import context
from backend.shared.models.base import SQLModel
from backend.shared.models.users import UserModel
from backend.shared.models.fails import FailModel
from backend.settings import settings

config = context.config

section = config.config_ini_section

config.set_section_option(section, "sqlalchemy.url", settings.dsn)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Запускает миграции в 'офлайн' режиме.

    Эта функция настраивает контекст только с URL
    и не с Engine, хотя Engine также приемлем
    здесь. Пропуская создание Engine,
    нам даже не нужен доступ к DBAPI.

    Вызовы context.execute() здесь выводят данную строку в
    выходной скрипт.

    Returns:
        None
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Выполняет миграции с использованием предоставленного соединения.

    Эта функция настраивает контекст с использованием
    соединения и метаданных целевой модели.

    Attributes:
        connection (Connection): Соединение с базой данных.
    
    Returns:
        None
    """
    context.configure(
    connection=connection, 
    target_metadata=target_metadata,
    compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Запускает миграции в 'онлайн' режиме асинхронно.

    В этом сценарии нам нужно создать Engine
    и ассоциировать соединение с контекстом.

    Returns:
        None
    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online():
    """Запускает миграции в 'онлайн' режиме.

    Эта функция проверяет, есть ли уже подключение,
    и в зависимости от этого запускает асинхронные
    или синхронные миграции.

    Returns:
        None
    """

    connectable = config.attributes.get("connection", None)

    if connectable is None:
        asyncio.run(run_async_migrations())
    else:
        do_run_migrations(connectable)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

