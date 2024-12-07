"""
Модуль для работы с неудачами (fail) в базе данных.

Этот модуль содержит класс `FailService`, который предоставляет методы для
взаимодействия с моделью неудачи в базе данных. Класс наследуется от
`BaseService` и использует асинхронные операции для работы с SQLAlchemy.

Класс `FailService` включает в себя метод для создания новой записи о неудаче.
"""
from typing import List
from logging import info
from sqlalchemy import select, func, text
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from bot.models import FailModel, UserModel, VoteModel
from .base import BaseService


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
        description: str,
        is_draft: bool = True
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
            rating=0,
            is_draft=is_draft
        )
        
        self.session.add(fail)
        await self.session.commit()
        await self.session.refresh(fail)
        
        info(f"Фейл ID={fail.id} создан пользователем {fail.user_id}: {name}")
        return fail

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
            .join(UserModel.fails)
            .where(FailModel.is_draft == False) # Только опубликованные
            .group_by(UserModel.id, UserModel.username)
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
            .where(FailModel.is_draft == False) # Только опубликованные
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
    
    async def get_user_fails(self, user_id: int) -> List[FailModel]:
        """
        Получает все опубликованные фейлы пользователя.
        
        Attributes:
            user_id (int): Идентификатор пользователя.

        Returns:
            List[FailModel]: Список фейлов пользователя.
        """

        query = (
            select(FailModel)
            .where(
                FailModel.user_id == user_id, 
                FailModel.is_draft == False
            )
            .order_by(FailModel.created_at.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def delete_fail(self, fail_id: int, user_id: int) -> None:
        """
        Удаляет фейл, если он принадлежит указанному пользователю.

        Attributes:
            fail_id (int): Идентификатор фейла.
            user_id (int): Идентификатор пользователя.

        Returns:
            None
        """
        fail = await self.get_fail_by_id(fail_id)
        if fail and fail.user_id == user_id:
            await self.session.delete(fail)
            await self.session.commit()
            info(f"Фейл ID={fail_id} успешно удален.")
            return True
        else:
            info(f"Фейл ID={fail_id} не найден или не принадлежит пользователю ID={user_id}.")
        return False
    
    async def check_user_vote(self, fail_id: int, user_id: int) -> VoteModel | None:
        """
        Проверяет, голосовал ли пользователь за этот фейл.

        Attributes:
            fail_id (int): Идентификатор фейла.
            user_id (int): Идентификатор пользователя.

        Returns:
            VoteModel | None: Объект голоса или None, если пользователь еще не голосовал.
        """
        query = (
            select(VoteModel)
            .where(
                VoteModel.fail_id == fail_id,
                VoteModel.user_id == user_id
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_rating(
        self, 
        fail_id: int, 
        user_id: int, 
        rating: int
    ) -> bool:
        """
        Обновляет рейтинг фейла, добавляя
        указанное значение к текущему рейтингу. 
        Только если пользователь еще не голосовал.

        Attributes:
            fail_id (int): Идентификатор фейла.
            user_id (int): Идентификатор пользователя.
            rating (int): Количество, на которое нужно изменить рейтинг.

        Returns:
            bool: True, если рейтинг успешно обновлен, False в противном случае.
            #! Ну, будем считать, что False - пользователь уже голосовал
        """
        # Проверяем предыдущий голос
        existing_vote = await self.check_user_vote(fail_id, user_id)
        if existing_vote:
            return False

        # Создаем новый голос
        vote = VoteModel(
            user_id=user_id,
            fail_id=fail_id,
            rating=rating
        )
        self.session.add(vote)

        # Обновляем рейтинг фейла
        try:
            fail = await self.get_fail_by_id(fail_id)
            if fail:
                fail.rating += rating
                await self.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            await self.session.rollback()
            info(f"Ошибка при обновлении рейтинга фейла ID={fail_id}: {e}")
            raise

    async def get_user_drafts(self, user_id: int) -> List[FailModel]:
        """
        Возвращает список черновиков фейлов (не опубликованных) для указанного пользователя.

        Attributes:
            user_id (int): Идентификатор пользователя.

        Returns:
            List[FailModel]: Список черновиков фейлов.
        """
        query = (
            select(FailModel)
            .where(
                FailModel.user_id == user_id, 
                FailModel.is_draft == True
            )
            .order_by(FailModel.created_at.desc())
        )
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def publish_draft(self, fail_id: int, user_id: int) -> bool:
        """
        Публикует черновик фейла, если он принадлежит указанному пользователю.

        Attributes:
            fail_id (int): Идентификатор фейла.
            user_id (int): Идентификатор пользователя.

        Returns:
            bool: True, если фейл успешно опубликован, False в противном случае.
        """
        fail = await self.get_fail_by_id(fail_id)
        if fail and fail.user_id == user_id and fail.is_draft:
            fail.is_draft = False
            await self.session.commit()
            return True
        return False