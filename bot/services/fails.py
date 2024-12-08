"""
Модуль для работы с неудачами (fail) в базе данных.

Этот модуль содержит класс `FailService`, который предоставляет методы для
взаимодействия с моделью неудачи в базе данных. Класс наследуется от
`BaseService` и использует асинхронные операции для работы с SQLAlchemy.

Класс `FailService` включает в себя метод для создания новой записи о неудаче.
"""
from typing import List, Tuple
from logging import info
from sqlalchemy import select, func, text
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from bot.models import FailModel, FailStatus, UserModel, VoteModel
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
        status: FailStatus = FailStatus.DRAFT
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
            status=status
        )
        
        self.session.add(fail)
        await self.session.commit()
        await self.session.refresh(fail)
        
        info(f"Фейл ID={fail.id} создан пользователем {fail.user_id}: {name}")
        return fail

    async def get_top_losers(self, limit: int = 10) -> List[Tuple[UserModel, int]]:
        """Получает список пользователей с наибольшим количеством неудач.

        Этот метод возвращает список пользователей, отсортированных по
        количеству неудач, с учетом заданного лимита.

        Attributes:
            limit (int): Максимальное количество пользователей для возврата.

        Returns:
            List[UserModel]: Список пользователей с наибольшим количеством неудач.
        
        Usage:
            users_with_ratings = await user_service.get_top_losers(10)
            for user, rating in users_with_ratings:
                print(f"User: {user.username}, Rating: {rating}")
        
        """
        query = (
            select(
                UserModel,
                func.coalesce(func.sum(FailModel.rating), 0).label('total_rating')
            )
            .outerjoin(UserModel.fails)
            .where(
                (FailModel.status == FailStatus.PUBLISHED) | 
                (FailModel.id.is_(None))
            ) 
            .group_by(UserModel.id)
            .order_by(text('total_rating DESC'))
            .limit(limit)
        )
        
        result = await self.session.execute(query)
        return result.all()
    
    async def to_draft(self, fail_id: int) -> bool:
        """
        Переводит фейл в статус черновика.

        Attributes:
            fail_id (int): Идентификатор фейла.

        Returns:
            bool: True если успешно переведен в черновик
        """
        fail = await self.get_fail_by_id(fail_id)
        if fail:
            fail.status = FailStatus.DRAFT
            await self.session.commit()
            info(f"Фейл ID={fail_id} переведен в черновик")
            return True
        return False

    async def get_fails_for_voting(self, limit: int = 5) -> List[FailModel]:
        """Получает случайные записи о неудачах для голосования.

        Attributes:
            limit (int): Максимальное количество неудач для возврата.

        Returns:
            List[FailModel]: Список случайных записей о неудачах.
        """
        query = (
            select(FailModel)
            .where(FailModel.status == FailStatus.PUBLISHED) # Только опубликованные
            .options(joinedload(FailModel.user))
            .order_by(func.random()) 
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().unique().all()

    async def get_fail_by_id(self, fail_id: int) -> FailModel | None:
        """Получает запись о неудаче по идентификатору.

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
                FailModel.status == FailStatus.PUBLISHED
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
                FailModel.status == FailStatus.DRAFT
            )
            .order_by(FailModel.created_at.desc())
        )
        info(f"Draft query: {query}")
        result = await self.session.execute(query)
        drafts = result.scalars().all()
        info(f"Draft results: {drafts}")
        return drafts
    
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
        if fail and fail.user_id == user_id and fail.status == FailStatus.DRAFT:
            fail.status = FailStatus.PUBLISHED
            await self.session.commit()
            return True
        return False
    
    async def update_draft(self, draft_id: int, name: str, description: str) -> bool:
        """
        Обновляет имя и описание черновика.
    
        Attributes:
            draft_id (int): ID черновика
            name (str): Новое имя
            description (str): Новое описание
    
        Returns:
            bool: True если успешно обновлено
        """
        fail = await self.get_fail_by_id(draft_id)
        if fail and fail.status == FailStatus.DRAFT:
            fail.name = name
            fail.description = description
            await self.session.commit()
            return True
        return False