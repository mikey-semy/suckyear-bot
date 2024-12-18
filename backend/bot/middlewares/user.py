"""
Модуль UserMiddleware

Этот модуль содержит класс UserMiddleware, который реализует
промежуточное ПО для обработки пользователей в приложении на
основе библиотеки aiogram. Он отвечает за создание или получение
пользователя в базе данных при получении сообщения от пользователя.
"""
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from sqlalchemy.ext.asyncio import AsyncSession
from backend.shared.services.users import UserService

class UserMiddleware(BaseMiddleware):
    """Промежуточное ПО для обработки пользователей.

    Этот класс отвечает за создание или получение пользователя
    в базе данных при получении сообщения от пользователя.

    Args:
        None
    """
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """Обрабатывает входящие события и вызывает обработчик.

        Если событие является сообщением, то происходит попытка
        получить или создать пользователя в базе данных.

        Args:
            handler (Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]]): 
                Обработчик события, который будет вызван после выполнения промежуточного ПО.
            event (TelegramObject): 
                Объект события, который содержит информацию о сообщении или другом событии.
            data (Dict[str, Any]): 
                Словарь, содержащий дополнительные данные, которые могут быть использованы
                в процессе обработки события.

        Returns:
            Any: Результат вызова обработчика.
        """
        if isinstance(event, Message):
            session = data.get("session")
            if session:
                user_service = UserService(session)
                await user_service.get_or_create_user(
                    chat_id=event.from_user.id,
                    username=event.from_user.username or str(event.from_user.id)
                )
        return await handler(event, data)
