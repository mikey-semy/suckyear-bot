"""
Модуль для определения схемы поста (post).

Этот модуль содержит классы `PostCreateSchema` и `PostSchema`, которые
используются для валидации и сериализации данных о постах. Классы
наследуются от `BaseSchema` и определяют структуру данных, связанных
с постами и пользователями.

Classes:
- PostCreateSchema: Схема для создания новой записи поста.
- PostSchema: Схема для представления данных поста, включая информацию о пользователе.
"""
from enum import Enum
from datetime import datetime
from pydantic import Field
from backend.shared.schemas.base import BaseSchema
from backend.shared.schemas.users import UserSchema

class PostStatus(str, Enum):
    DRAFT = "draft"
    CHECKING = "checking"
    PUBLISHED = "published"
    DELETED = "deleted"
    
class PostCreateSchema(BaseSchema):
    """
    Схема для создания новой записи поста.

    Этот класс определяет структуру данных, необходимых для создания
    новой записи поста, включая название и контекст.

    Attributes:
        name (str): Название поста (максимум 100 символов).
        short_context (str): Краткий контекст поста (максимум 100 символов).
        full_context (str): Полный контекст поста (максимум 1000 символов).
    """
    name: str = Field(max_length=100)
    content: str = Field(max_length=1000)
    status: PostStatus = PostStatus.DRAFT
    
class PostSchema(PostCreateSchema):
    """
    Схема для представления данных поста.

    Этот класс расширяет `PostCreateSchema`, добавляя дополнительные
    поля, такие как идентификатор, ID пользователя и временные метки.

    Attributes: 
        id (int): Уникальный идентификатор поста.
        user_id (int): ID пользователя, связанного с постом.
        rating (int): Количество голосов (по умолчанию 0).
        created_at (datetime): Дата и время создания записи поста.
        updated_at (datetime): Дата и время последнего обновления записи поста.
        user (UserSchema): Схема пользователя, связанного с постом.
    """
    id: int
    user_id: int
    rating: int = 0
    created_at: datetime
    updated_at: datetime
    user: UserSchema
