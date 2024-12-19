from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from backend.shared.models.base import SQLModel
from backend.shared.models.types import TYPE_CHECKING

if TYPE_CHECKING:
    from .posts import PostModel

class TagModel(SQLModel):
    """
    Модель для тегов
    
    Args:
        name (str): Название тега.
        posts (List[PostModel]): Список постов, связанных с тегом.
    """
    name: Mapped[str] = mapped_column(String(50), unique=True)
    
    posts: Mapped[List["PostModel"]] = relationship(secondary="post_tags", back_populates="tags")