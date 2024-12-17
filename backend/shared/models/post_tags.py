from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from backend.shared.models.base import SQLModel


class PostTagModel(SQLModel):
    """
    Промежуточная таблица для связи постов и тегов
    
    Attributes:
        post_id (int): Идентификатор поста
        tag_id (int): Идентификатор тега
    """
    __tablename__ = "post_tags"

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)