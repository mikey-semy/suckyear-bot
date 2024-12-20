"""
Модуль для определения базового сервиса для работы с базой данных.

Этот модуль содержит класс `BaseService`, который предоставляет общую
инфраструктуру для работы с асинхронными сессиями SQLAlchemy. Класс
предназначен для использования в других сервисах, которые будут
взаимодействовать с моделями базы данных.

Класс `BaseService` включает в себя инициализацию сессии базы данных.
"""
from typing import TypeVar, Generic, Type, Any, List
import logging
from sqlalchemy import select, func, desc, asc
from sqlalchemy.sql.expression import Executable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from shared.schemas.base import BaseSchema, PaginationParams
from shared.models.base import SQLModel

M = TypeVar("M", bound=SQLModel)
T = TypeVar("T", bound=BaseSchema)

class SessionMixin:
    """
    Миксин для предоставления экземпляра сессии базы данных.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализирует SessionMixin.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
        """
        self.session = session

class BaseService(SessionMixin):
    """
    Базовый класс для сервисов приложения.
    """

class BaseDataManager(SessionMixin, Generic[T]):
    """
    Базовый класс для менеджеров данных с поддержкой обобщенных типов.
    
    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
        schema (Type[T]): Тип схемы данных.
        model (Type[M]): Тип модели.
    """
    def __init__(self, session:AsyncSession, schema: Type[T], model: Type[M]):
        """
        Инициализирует BaseDataManager.

        Args:
            session (AsyncSession): Асинхронная сессия базы данных.
            schema (Type[T]): Тип схемы данных.
            model (Type[M]): Тип модели.
        """
        super().__init__(session)
        self.schema = schema
        self.model = model

    async def add_one(self, model: Any) -> T:
        """
        Добавляет одну запись в базу данных.

        Args:
            model (Any): Модель для добавления.

        Returns:
            T: Добавленная запись в виде схемы.
        
        Raises:
            SQLAlchemyError: Если произошла ошибка при добавлении.
        """
        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
            return self.schema(**model.to_dict())
        except SQLAlchemyError as e:
            await self.session.rollback()
            logging.error("Ошибка при добавлении: %s", e)
            raise

    async def update_one(self, model_to_update, updated_model: Any) -> T | None:
        """
        Обновляет одну запись в базе данных.

        Args:
            model_to_update: Модель для обновления.
            updated_model (Any): Обновленная модель.

        Returns:
            T | None: Обновленная запись в виде схемы или None, если запись не найдена.
        
        Raises: 
            SQLAlchemyError: Если произошла ошибка при обновлении.
        """
        try:
            if not model_to_update:
                return None

            for key, value in updated_model.to_dict().items():
                if key != "id":
                    setattr(model_to_update, key, value)

            await self.session.commit()
            await self.session.refresh(model_to_update)
            return self.schema(**model_to_update.to_dict())
        except SQLAlchemyError as e:
            await self.session.rollback()
            logging.error("Ошибка при обновлении: %s", e)
            raise

    async def delete_one(self, delete_statement: Executable) -> bool:
        """
        Удаляет одну запись из базы данных.

        Args:
            delete_statement (Executable): SQL-запрос для удаления.

        Returns:
            bool: True, если запись удалена, False в противном случае.
        
        Raises:
            SQLAlchemyError: Если произошла ошибка при удалении.
        """
        try:
            delete_statement = delete_statement.limit(1)
            result = await self.session.execute(delete_statement)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            logging.error("Ошибка при удалении: %s", e)
            return False

    async def delete_all(self, delete_statement: Executable) -> bool:
        """
        Удаляет все записи из базы данных, соответствующие заданному запросу.

        Args:
            delete_statement (Executable): SQL-запрос для удаления.

        Returns:
            bool: True, если записи удалены, False в противном случае.
        
        Raises:
            SQLAlchemyError: Если произошла ошибка при удалении.
        """
        try:
            result = await self.session.execute(delete_statement)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            logging.error("Ошибка при удалении: %s", e)
            return False

    async def get_one(self, select_statement: Executable) -> Any | None:
        """
        Получает одну запись из базы данных.

        Args:
            select_statement (Executable): SQL-запрос для выборки.

        Returns:
            Any | None: Полученная запись или None, если запись не найдена.
        
        Raises: 
            SQLAlchemyError: Если произошла ошибка при получении записи.
        """
        try:
            result = await self.session.execute(select_statement)
            return result.scalar()
        except SQLAlchemyError as e:
            logging.error("Ошибка при получении записи: %s", e)
            return None

    async def get_all(self, select_statement: Executable) -> List[T]:
        """
        Получает все записи из базы данных.
    
        Args:
            select_statement (Executable): SQL-запрос для выборки.
    
        Returns:
            List[T]: Список всех записей.  
        
        Raises:
            SQLAlchemyError: Если произошла ошибка при получении записей.
        """
        try:
            result = await self.session.execute(select_statement)
            items = result.unique().scalars().all()
            return [self.schema.model_validate(item) for item in items]
        except SQLAlchemyError as e:
            logging.error("Ошибка при получении записей: %s", e)
            return []

    async def get_paginated(
        self,
        select_statement: Executable,
        pagination: PaginationParams,
    ) -> tuple[List[T], int]:
        """
        Получает пагинированные записи из базы данных.

        Args:
            select_statement (Executable): SQL-запрос для выборки.
            pagination (PaginationParams): Параметры пагинации.

        Returns:
            tuple[List[T], int]: Список пагинированных записей и общее количество записей.
        
        Raises:
            SQLAlchemyError: Если произошла ошибка при получении пагинированных записей.
        """
        try:
            total = await self.session.scalar(
                select(func.count()).select_from(select_statement.subselect_statement())
            )

            sort_column = getattr(self.model, pagination.sort_by)

            select_statement = select_statement.order_by(
                desc(sort_column) if pagination.sort_desc else asc(sort_column)
            )

            select_statement = select_statement.offset(pagination.skip).limit(pagination.limit)

            items = await self.get_all(select_statement)

            return items, total
        except SQLAlchemyError as e:
            logging.error("Ошибка при получении пагинированных записей: %s", e)
            return [], 0
