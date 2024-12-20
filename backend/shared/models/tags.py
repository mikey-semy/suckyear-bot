from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from shared.models.base import SQLModel
from shared.models.types import TYPE_CHECKING

if TYPE_CHECKING:
    from .posts import Post

class Tag(SQLModel):
    """
    Модель для тегов
    
    Args:
        name (str): Название тега.
        posts (List[Post]): Список постов, связанных с тегом.
    """
    name: Mapped[str] = mapped_column(String(50), unique=True)
    
    posts: Mapped[List["Post"]] = relationship(secondary="posttags", back_populates="tags")