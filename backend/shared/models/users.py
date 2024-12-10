"""
Модуль, содержащий модели данных для работы с пользователями.

Этот модуль определяет следующие модели SQLAlchemy:
- UserModel: представляет пользователя в системе.

Модель наследуется от базового класса SQLModel и определяет 
соответствующие поля и отношения между таблицами базы данных.

Модель использует типизированные аннотации Mapped для определения полей,
что обеспечивает улучшенную поддержку статической типизации.

Этот модуль предназначен для использования в сочетании с SQLAlchemy ORM
для выполнения операций с базой данных, связанных с пользователями.
"""
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, BigInteger
from backend.shared.models.base import SQLModel
from backend.shared.models.types import TYPE_CHECKING
if TYPE_CHECKING:
    from .fails import FailModel
    from .votes import VoteModel
    
    
class UserModel(SQLModel):
    """
    Модель для представления пользователей.

    Attributes:
        id (int): Уникальный идентификатор пользователя.
        chat_id (int): Уникальный идентификатор чата пользователя.
        username (str): Имя пользователя.
        fails (List[FailModel]): Список фейловых историй, связанных с пользователем.
    """
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column("chat_id", BigInteger, unique=True)
    username: Mapped[str] = mapped_column("username", String(100))
    fails: Mapped[List["FailModel"]] = relationship(back_populates="user")
    votes: Mapped[List["VoteModel"]] = relationship(back_populates="user")