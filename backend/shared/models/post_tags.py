from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, UniqueConstraint
from shared.models.base import SQLModel


class PostTag(SQLModel):
    """
    Промежуточная таблица для связи постов и тегов
    
    Args:
        post_id (int): Идентификатор поста
        tag_id (int): Идентификатор тега
    """

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
    
    __table_args__ = (
        UniqueConstraint('post_id', 'tag_id', name='uq_post_tag'),
    )