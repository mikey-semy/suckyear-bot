from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey
from backend.shared.models.base import SQLModel
from backend.shared.models.types import TYPE_CHECKING
if TYPE_CHECKING:
    from .users import UserModel
    from .posts import PostModel
    
class VoteModel(SQLModel):
    """
    Модель для представления голосов пользователей за посты.

    Attributes:
        id (int): Уникальный идентификатор голоса.
        user_id (int): Идентификатор пользователя, который оставил голос.
        post_id (int): Идентификатор поста, за который был оставлен голос.
        rating (int): Рейтинг, присвоенный посту пользователем.
        created_at (datetime): Дата и время создания записи голоса.
    """
    __tablename__ = "votes"
    
    id: Mapped[int] = mapped_column("id", primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    rating: Mapped[int] = mapped_column("rating", Integer, default=0)
    created_at: Mapped[datetime] = mapped_column("created_at", default=datetime.now)

    user: Mapped["UserModel"] = relationship(back_populates="votes")
    post: Mapped["PostModel"] = relationship(back_populates="votes")