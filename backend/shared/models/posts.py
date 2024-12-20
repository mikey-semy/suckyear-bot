"""
Модуль, содержащий модели данных для работы с инструкциями по эксплуатации.

Этот модуль определяет следующие модели SQLAlchemy:
- Post: представляет инструкцию по эксплуатации

Модель наследуется от базового класса SQLModel и определяет 
соответствующие поля и отношения между таблицами базы данных.

Модель использует типизированные аннотации Mapped для определения полей,
что обеспечивает улучшенную поддержку статической типизации.

Этот модуль предназначен для использования в сочетании с SQLAlchemy ORM
для выполнения операций с базой данных, связанных с инструкциями по эксплуатации.
"""

from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from shared.models.base import SQLModel
from shared.schemas.posts import PostStatus
from shared.models.types import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .votes import Vote
    from .tags import Tag
class Post(SQLModel):
    """
    Модель для представления постовых историй.

    Args:
        name (str): Название поста.
        author (int): Идентификатор пользователя, связанного с постом.
        content (str): Подробное описание поста.
        rating (int): Рейтинг поста, основанный на голосах пользователей.
        status (PostStatus): Статус поста.
        
        user (User): Пользователь, связанный с постом.
        votes (List[Vote]): Список голосов, связанных с постом.
        tags (List[Tag]): Список тегов, связанных с постом.
    """

    name: Mapped[str] = mapped_column(String(100))
    author: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(String(1000))
    rating: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[PostStatus] = mapped_column(default=PostStatus.DRAFT)
    
    user: Mapped["User"] = relationship(back_populates="posts")
    votes: Mapped[List["Vote"]] = relationship(back_populates="post", cascade="all, delete")
    tags: Mapped[List["Tag"]] = relationship(secondary="posttags", back_populates="posts")