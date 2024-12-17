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
from sqlalchemy.sql.expression import Executable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from backend.shared.schemas.base import BaseSchema
from backend.shared.models.base import SQLModel

M = TypeVar("M", bound=SQLModel)
T = TypeVar("T", bound=BaseSchema)

class SessionMixin:
    """
    Миксин для предоставления экземпляра сессии базы данных.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализирует SessionMixin.

        Attributes:
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
    """
    def __init__(self, session:AsyncSession, schema: Type[T]):
        """
        Инициализирует BaseDataManager.

        Attributes:
            session (AsyncSession): Асинхронная сессия базы данных.
            schema (Type[T]): Тип схемы данных.
        """
        super().__init__(session)
        self.schema = schema

    async def add_one(self, model: Any) -> T:
        """
        Добавляет одну запись в базу данных.

        Attributes:
            model (Any): Модель для добавления.

        Returns:
            T: Добавленная запись в виде схемы.
        """
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self.schema(**model.to_dict)

    async def update_one(self, model_to_update, updated_model: Any) -> T | None:
        """
        Обновляет одну запись в базе данных.

        Attributes:
            model_to_update: Модель для обновления.
            updated_model (Any): Обновленная модель.

        Returns:
            T | None: Обновленная запись в виде схемы или None, если запись не найдена.
        """
        if model_to_update:
            updated_model_dict = updated_model.to_dict
            for key, value in updated_model_dict.items():
                if key != "id":
                    setattr(model_to_update, key, value)
        else:
            return None
        await self.session.commit()
        await self.session.refresh(model_to_update)
        return self.schema(**model_to_update.to_dict)

    async def delete_one(self, delete_statement: Executable) -> bool:
        """
        Удаляет одну запись из базы данных.

        Attributes:
            delete_statement (Executable): SQL-запрос для удаления.

        Returns:
            bool: True, если запись удалена, False в противном случае.
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

        Attributes:
            delete_statement (Executable): SQL-запрос для удаления.

        Returns:
            bool: True, если записи удалены, False в противном случае.
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

        Attributes:
            select_statement (Executable): SQL-запрос для выборки.

        Returns:
            Any | None: Полученная запись или None, если запись не найдена.
        """
        result = await self.session.execute(select_statement)
        return result.scalar()

    async def get_all(self, select_statement: Executable) -> List[Any]:
        """
        Получает все записи из базы данных по заданному запросу.

        Attributes:
            select_statement (Executable): SQL-запрос для выборки.

        Returns:
            List[Any]: Список полученных записей.
        """
        result = await self.session.execute(select_statement)
        return list(result.unique().scalars().all())