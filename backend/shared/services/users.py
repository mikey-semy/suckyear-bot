"""
Модуль для работы с пользователями в базе данных.

Этот модуль содержит класс `UserService`, который предоставляет методы для
взаимодействия с моделью пользователя в базе данных. Класс наследуется от
`BaseService` и использует асинхронные операции для работы с SQLAlchemy.

Класс `UserService` включает в себя методы для получения пользователя по
ID чата, создания нового пользователя и получения или создания пользователя
в зависимости от его наличия в базе данных.
"""
from logging import info
from sqlalchemy import select
from backend.shared.models import UserModel
from .base import BaseService

class UserService(BaseService):
    """
    Сервис для работы с пользователями.

    Этот класс предоставляет методы для получения, создания и управления
    пользователями в базе данных.

    Attributes:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
    """
    async def get_by_chat_id(self, chat_id: int) -> UserModel | None:
        """
        Получает пользователя по ID чата.

        :param chat_id: ID чата пользователя.
        :return: Экземпляр UserModel или None, если пользователь не найден.
        """
        query = select(UserModel).where(UserModel.chat_id == chat_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        info(f"Найден пользователь: {user.id if user else None} с ID чата: {chat_id}")
        return user
    
    async def create_user(self, chat_id: int, username: str) -> UserModel:
        """
        Создает нового пользователя в базе данных.

        :param chat_id: ID чата пользователя.
        :param username: Имя пользователя.
        :return: Экземпляр созданного UserModel.
        """
        user = UserModel(
            chat_id=chat_id,
            username=username
        )
        self.session.add(user)
        await self.session.commit()
        return user
        
    async def get_or_create_user(self, chat_id: int, username: str) -> UserModel:
        """
        Получает пользователя по ID чата или создает нового, если он не существует.

        :param chat_id: ID чата пользователя.
        :param username: Имя пользователя.
        :return: Экземпляр UserModel.
        """
        user = await self.get_by_chat_id(chat_id)
        if not user:
            user = await self.create_user(chat_id, username)
        return user
