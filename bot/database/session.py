"""
Модуль для работы с асинхронными сессиями SQLAlchemy.

Этот модуль определяет асинхронный движок базы данных и сессию для выполнения
операций с базой данных в асинхронном режиме. Он использует настройки, 
определенные в конфигурации приложения.

Модуль предоставляет функцию для получения асинхронной сессии, которая 
может быть использована в асинхронных функциях для выполнения операций 
с базой данных.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bot.config import settings

# Создание асинхронного движка базы данных
engine = create_async_engine(
    url=settings.dsn, 
    echo=True,
    pool_pre_ping=True
)

# Создание фабрики асинхронных сессий
async_session = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Получение асинхронной сессии для работы с базой данных.

    Эта функция создает асинхронную сессию, которая может быть использована
    для выполнения операций с базой данных. Сессия автоматически закрывается
    после завершения работы с ней.

    Yields:
        AsyncSession: Асинхронная сессия для работы с базой данных.
    """
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
