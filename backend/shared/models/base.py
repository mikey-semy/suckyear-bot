"""
Модуль base.py содержит базовые классы и типы данных для работы с моделями SQLAlchemy.

Этот модуль предоставляет:
1. SQLModel - базовый класс для определения моделей SQLAlchemy с дополнительными методами.
2. ArrayOfStrings - пользовательский тип данных для работы с массивами строк, 
   обеспечивающий совместимость между различными диалектами баз данных.

Классы:
- SQLModel: Базовый класс для моделей с методами для работы со схемой, именем таблицы и полями.
- ArrayOfStrings: Тип данных для хранения массивов строк, адаптирующийся под разные диалекты SQL.

Модуль обеспечивает удобную работу с моделями данных и их преобразование в различные форматы.
"""
from datetime import datetime
import json
from typing import Any, Dict, List, Type, TypeVar, Optional
from sqlalchemy import MetaData, Dialect, Integer, TIMESTAMP
from sqlalchemy.types import ARRAY, TypeDecorator, Text, JSON
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.declarative import declared_attr

T = TypeVar('T', bound='SQLModel')

class SQLModel(DeclarativeBase):
    """
    Базовый класс, используемый для определения моделей.

    Предоставляет удобные методы, которые можно использовать для
    преобразования модели в соответствующую схему.
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
        onupdate=datetime.now
    )
    
    metadata = MetaData()
    
    @declared_attr
    def __tablename__(self: Type[T]) -> str:
        """
        Возвращает имя таблицы для модели.

        Returns:
            str: Имя таблицы в нижнем регистре и во множественном числе.
        """
        return self.__name__.lower() + 's'

    @classmethod
    def fields(cls: Type[T]) -> List[str]:
        """
        Возвращает список имен полей модели.

        Returns:
            List[str]: Список имен полей.
        """

        return cls.__mapper__.selectable.c.keys()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует экземпляр модели в словарь.

        Returns:
            Dict[str, Any]: Словарь, представляющий модель.
        """

        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        """
        Строковое представление экземпляра модели для удобства отладки.
        Содержит идентификатор, дату создания и дату последнего обновления.
        
        Returns:
            str: Строковое представление экземпляра модели.
        """
        return f"<{self.__class__.__name__}(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>"
    
class ArrayOfStrings(TypeDecorator):
    """
    Пользовательский тип данных для работы с массивами строк.

    Этот класс обеспечивает совместимость между различными диалектами баз данных,
    используя ARRAY для PostgreSQL и JSON для других диалектов.
    """
    impl = Text
    cache_ok = True

    def load_dialect_impl(self, dialect: Dialect) -> TypeDecorator:
        """
        Загружает соответствующую реализацию для конкретного диалекта базы данных.

        Args:
            dialect: Диалект базы данных.

        Returns:
            Реализация типа данных для конкретного диалекта.
        """
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(ARRAY(Text()))
        else:
            return dialect.type_descriptor(JSON())

    def process_bind_param(self, value: Optional[List[str]], dialect: Dialect) -> Optional[str]:
        """
        Обрабатывает параметр при привязке к базе данных.

        Args:
            value: Значение для обработки.
            dialect: Диалект базы данных.

        Returns:
            Обработанное значение.
        """
        if dialect.name == 'postgresql':
            return value
        if value is not None:
            return json.dumps(value)

    def process_result_value(self, value: Optional[str], dialect: Dialect) -> Optional[List[str]]:
        """
        Обрабатывает значение, полученное из базы данных.

        Args:
            value: Значение для обработки.
            dialect: Диалект базы данных.

        Returns:
            Обработанное значение.
        """
        if dialect.name == 'postgresql':
            return value
        if value is not None:
            return json.loads(value)

    def process_literal_param(self, value: Optional[List[str]], dialect: Dialect) -> Optional[List[str]]:
        """
        Обрабатывает литеральный параметр.

        Args:
            value: Значение для обработки.
            dialect: Диалект базы данных.

        Returns:
            Обработанное значение.
        """
        return value

    @property
    def python_type(self) -> Type[list]:
        return list

