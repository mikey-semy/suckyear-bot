"""
Модуль для реализации промежуточного программного обеспечения (middleware) 
для работы с базой данных в приложении на основе aiogram.

Этот модуль определяет класс `DatabaseMiddleware`, который добавляет 
асинхронную сессию базы данных в контекст обработки событий Telegram. 
Это позволяет обработчикам событий использовать сессию для выполнения 
операций с базой данных.

Класс наследуется от `BaseMiddleware` и переопределяет метод `__call__`,
чтобы обеспечить доступ к сессии базы данных.
"""
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.session import async_session

class DatabaseMiddleware(BaseMiddleware):
    """
    Промежуточное программное обеспечение для работы с базой данных.

    Этот класс добавляет асинхронную сессию базы данных в контекст 
    обработки событий Telegram, позволяя обработчикам использовать 
    сессию для выполнения операций с базой данных.

    Attributes:
        handler (Callable): Обработчик события Telegram.
        event (TelegramObject): Объект события Telegram.
        data (Dict[str, Any]): Словарь данных, передаваемых в обработчик.
    """
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        Обработка события Telegram с добавлением сессии базы данных.

        Этот метод создает асинхронную сессию базы данных и добавляет 
        ее в словарь данных, передаваемых в обработчик. После этого 
        вызывается обработчик события.

        Attributes:
            handler (Callable): Обработчик события Telegram.
            event (TelegramObject): Объект события Telegram.
            data (Dict[str, Any]): Словарь данных, передаваемых в обработчик.

        Returns:
            Any: Результат выполнения обработчика.
        """
        async with async_session() as session:
            data["session"] = session
            return await handler(event, data)
