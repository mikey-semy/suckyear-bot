"""
Модуль для работы с неудачами (fail) в базе данных.

Этот модуль содержит класс `FailService`, который предоставляет методы для
взаимодействия с моделью неудачи в базе данных. Класс наследуется от
`BaseService` и использует асинхронные операции для работы с SQLAlchemy.

Класс `FailService` включает в себя метод для создания новой записи о неудаче.
"""
from typing import List
from sqlalchemy import select, func, text
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models import FailModel, UserModel
from bot.schemas.fails import FailCreateSchema
from .base import BaseService
from logging import info

class FailService(BaseService):
    """
    Сервис для работы с неудачами.

    Этот класс предоставляет методы для создания и управления записями о неудачах
    в базе данных.

    Attributes:
        session (AsyncSession): Асинхронная сессия для работы с базой данных.
    """
    async def create_fail(
        self, 
        user_id: int, 
        name: str, 
        description: str
    ) -> FailModel:
        """Создает новую запись о неудаче.

        Этот метод создает новую запись о неудаче в базе данных
        с указанными параметрами.

        Attributes:
            user_id (int): Идентификатор пользователя, связанного с неудачей.
            name (str): Название неудачи.
            description (str): Описание неудачи.

        Returns:
            FailModel: Созданная запись о неудаче.
        """
        info(f"Создание фейла для пользователя {user_id}: {name}")
        
        user_query = select(UserModel).where(UserModel.id == user_id)
        user = await self.session.execute(user_query)
        user = user.scalar_one_or_none()

        if not user:
            raise ValueError(f"User with id {user_id} not found")
        
        fail = FailModel(
            user_id=user_id,
            name=name,
            description=description,
            rating=0
        )
        
        self.session.add(fail)
        await self.session.commit()
        await self.session.refresh(fail)
        
        info(f"Фейл ID={fail.id} создан пользователем {fail.user_id}: {name}")
        return fail

    async def debug_relationships(self):
        """Проверяет пользователей и их неудачи."""
        users_query = (
            select(UserModel)
            .options(joinedload(UserModel.fails))
        )
        users = await self.session.execute(users_query)
        users_list = users.unique().scalars().all()

        info("\n=== DEBUG RELATIONSHIPS ===")
        for user in users_list:
            info(f"\nUser: {user.username} (ID: {user.id})")
            info(f"Fails count: {len(user.fails)}")
            for fail in user.fails:
                info(f"- Fail: {fail.name} (rating: {fail.rating})")
    
    async def debug_fails(self):
        """Выводит информацию о всех неудачах."""
        fails_query = select(FailModel)
        result = await self.session.execute(fails_query)
        fails = result.scalars().all()
        info("\n=== DEBUG FAILS ===")
        for fail in fails:
            info(f"Fail ID: {fail.id}, User ID: {fail.user_id}, Name: {fail.name}")
    async def get_top_losers(self, limit: int = 10) -> List[UserModel]:
        """Получает список пользователей с наибольшим количеством неудач.

        Этот метод возвращает список пользователей, отсортированных по
        количеству неудач, с учетом заданного лимита.

        Attributes:
            limit (int): Максимальное количество пользователей для возврата.

        Returns:
            List[UserModel]: Список пользователей с наибольшим количеством неудач.
        """
        query = (
            select(
                UserModel,
                func.coalesce(func.sum(FailModel.rating), 0).label('total_rating')
            )
            .join(UserModel.fails)  # Changed back to inner join
            .group_by(UserModel.id, UserModel.username)  # Add all non-aggregated columns
            .order_by(text('total_rating DESC'))
            .limit(limit)
        )
        
        result = await self.session.execute(query)
        return result.unique().all()
    
    async def get_fails_for_voting(self, limit: int = 5) -> List[FailModel]:
        """Получает случайные записи о неудачах для голосования.

        Этот метод возвращает случайные записи о неудачах, которые могут
        быть использованы для голосования, с учетом заданного лимита.

        Attributes:
            limit (int): Максимальное количество неудач для возврата.

        Returns:
            List[FailModel]: Список случайных записей о неудачах.
        """
        query = (
            select(FailModel)
            .options(joinedload(FailModel.user))
            .order_by(func.random()) 
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.unique().scalars().all()

    async def get_fail_by_id(self, fail_id: int) -> FailModel | None:
        """Получает запись о неудаче по идентификатору.

        Этот метод возвращает запись о неудаче, соответствующую
        указанному идентификатору.

        Attributes:
            fail_id (int): Идентификатор неудачи.

        Returns:
            FailModel: Запись о неудаче или None, если неудача не найдена.
        """
        query = (
            select(FailModel)
            .options(joinedload(FailModel.user))
            .where(FailModel.id == fail_id)
        )
        result = await self.session.execute(query)
 
        return result.scalar_one_or_none()

    async def update_rating(self, fail_id: int, rating: int) -> None:
        """Обновляет рейтинг записи о неудаче.

        Этот метод обновляет рейтинг записи о неудаче, добавляя
        указанное значение к текущему рейтингу.

        Attributes:
            fail_id (int): Идентификатор неудачи, рейтинг которой нужно обновить.
            rating (int): Значение, которое будет добавлено к текущему рейтингу.

        Returns:
            None
        """
        try:
            fail = await self.get_fail_by_id(fail_id)
            if fail:
                fail.rating += rating
                await self.session.commit()
                info(f"Рейтинг фейла ID={fail.id} обновлен на {rating}. Новый рейтинг: {fail.rating}")
                return True
            info(f"Не удалось найти фейл с ID={fail_id} для обновления рейтинга.")
            return False
        except SQLAlchemyError as e:
            await self.session.rollback()
            info(f"Ошибка при обновлении рейтинга фейла ID={fail_id}: {e}")
            raise