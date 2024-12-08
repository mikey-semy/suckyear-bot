"""
Модуль, содержащий модели данных для работы с инструкциями по эксплуатации.

Этот модуль определяет следующие модели SQLAlchemy:
- FailModel: представляет инструкцию по эксплуатации

Модель наследуется от базового класса SQLModel и определяет 
соответствующие поля и отношения между таблицами базы данных.

Модель использует типизированные аннотации Mapped для определения полей,
что обеспечивает улучшенную поддержку статической типизации.

Этот модуль предназначен для использования в сочетании с SQLAlchemy ORM
для выполнения операций с базой данных, связанных с инструкциями по эксплуатации.
"""
from datetime import datetime
from enum import Enum
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from bot.models.base import SQLModel
from bot.models.types import TYPE_CHECKING
if TYPE_CHECKING:
    from .users import UserModel
    from .votes import VoteModel

class FailStatus(str, Enum):
    """
    Статус фейла.
    
    Attributes:
        DRAFT (str): Черновик фейла.
        CHECKING (str): Фейл на проверке.
        PUBLISHED (str): Опубликованный фейл.
    """
    DRAFT = "draft"
    CHECKING = "checking"
    PUBLISHED = "published"

class FailModel(SQLModel):
    """
    Модель для представления фейловых историй.

    Attributes:
        id (int): Уникальный идентификатор фейла.
        user_id (int): Идентификатор пользователя, связанного с фейлом.
        created_at (datetime): Дата и время создания записи.
        updated_at (datetime): Дата и время последнего обновления записи.
        name (str): Название фейла.
        description (str): Подробное описание фейла.
        rating (int): Рейтинг фейла, основанный на голосах пользователей.
        status (FailStatus): Статус фейла.
    """
    __tablename__ = "fails"

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column("created_at", default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column("updated_at", default=datetime.now, onupdate=datetime.now)
    name: Mapped[str] = mapped_column("name", String(100))
    description: Mapped[str] = mapped_column("description", String(1000))
    rating: Mapped[int] = mapped_column("rating", Integer, default=0)
    status: Mapped[FailStatus] = mapped_column(default=FailStatus.DRAFT)
    
    user: Mapped["UserModel"] = relationship(back_populates="fails")
    votes: Mapped[List["VoteModel"]] = relationship(back_populates="fail", cascade="all, delete")
