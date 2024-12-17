from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from backend.shared.models.base import SQLModel
from backend.shared.models.posts import PostModel

class TagModel(SQLModel):
    """
    Модель для тегов
    
    Attributes:
        id (int): Уникальный идентификатор тега.
        name (str): Название тега.
        posts (List[PostModel]): Список постов, связанных с тегом.
    """
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    name: Mapped[str] = mapped_column("name", String(50), unique=True)
    posts: Mapped[List["PostModel"]] = relationship(secondary="post_tags", back_populates="tags")