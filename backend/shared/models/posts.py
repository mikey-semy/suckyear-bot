"""
Модуль, содержащий модели данных для работы с инструкциями по эксплуатации.

Этот модуль определяет следующие модели SQLAlchemy:
- PostModel: представляет инструкцию по эксплуатации

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
from backend.shared.models.base import SQLModel
from backend.shared.models.tags import TagModel
from backend.shared.models.types import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import UserModel
    from .votes import VoteModel

class PostStatus(str, Enum):
    """
    Статус поста.
   
    Attributes:
        DRAFT (str): Черновик поста.
        CHECKING (str): Пост на проверке.
        PUBLISHED (str): Опубликованный пост.
        DELETED (str): Удаленный пост.
    """
    DRAFT = "draft"
    CHECKING = "checking" 
    PUBLISHED = "published"
    DELETED = "deleted"

class PostModel(SQLModel):
    """
    Модель для представления постовых историй.

    Attributes:
        id (int): Уникальный идентификатор поста.
        user_id (int): Идентификатор пользователя, связанного с постом.
        created_at (datetime): Дата и время создания записи.
        updated_at (datetime): Дата и время последнего обновления записи.
        name (str): Название поста.
        content (str): Подробное описание поста.
        rating (int): Рейтинг поста, основанный на голосах пользователей.
        status (PostStatus): Статус поста.
        
        user (UserModel): Пользователь, связанный с постом.
        votes (List[VoteModel]): Список голосов, связанных с постом.
        tags (List[TagModel]): Список тегов, связанных с постом.
    """
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column("created_at", default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column("updated_at", default=datetime.now, onupdate=datetime.now)
    name: Mapped[str] = mapped_column("name", String(100))
    content: Mapped[str] = mapped_column("description", String(1000))
    rating: Mapped[int] = mapped_column("rating", Integer, default=0)
    status: Mapped[PostStatus] = mapped_column(default=PostStatus.DRAFT)
    
    user: Mapped["UserModel"] = relationship(back_populates="posts")
    votes: Mapped[List["VoteModel"]] = relationship(back_populates="post", cascade="all, delete")
    tags: Mapped[List["TagModel"]] = relationship(secondary="post_tags", back_populates="posts")