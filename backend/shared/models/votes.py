from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from shared.models.base import SQLModel
from shared.models.types import TYPE_CHECKING
if TYPE_CHECKING:
    from .users import UserModel
    from .posts import PostModel
    
class VoteModel(SQLModel):
    """
    Модель для представления голосов пользователей за посты.

    Args:
        user_id (int): Идентификатор пользователя, который оставил голос.
        post_id (int): Идентификатор поста, за который был оставлен голос.
        rating (int): Рейтинг, присвоенный посту пользователем.
    """
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    rating: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["UserModel"] = relationship(back_populates="votes")
    post: Mapped["PostModel"] = relationship(back_populates="votes")