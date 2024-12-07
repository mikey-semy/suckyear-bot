"""
Модуль для определения схемы неудачи (fail).

Этот модуль содержит классы `FailCreateSchema` и `FailSchema`, которые
используются для валидации и сериализации данных о неудачах. Классы
наследуются от `BaseSchema` и определяют структуру данных, связанных
с неудачами и пользователями.

Classes:
- FailCreateSchema: Схема для создания новой записи о неудаче.
- FailSchema: Схема для представления данных о неудаче, включая информацию о пользователе.
"""
from datetime import datetime
from pydantic import Field
from bot.schemas.base import BaseSchema
from bot.schemas.users import UserSchema

class FailCreateSchema(BaseSchema):
    """
    Схема для создания новой записи о неудаче.

    Этот класс определяет структуру данных, необходимых для создания
    новой записи о неудаче, включая название и контекст.

    Attributes:
        name (str): Название неудачи (максимум 100 символов).
        short_context (str): Краткий контекст неудачи (максимум 100 символов).
        full_context (str): Полный контекст неудачи (максимум 1000 символов).
    """
    name: str = Field(max_length=100)
    short_context: str = Field(max_length=100)
    full_context: str = Field(max_length=1000)
    
class FailSchema(FailCreateSchema):
    """
    Схема для представления данных о неудаче.

    Этот класс расширяет `FailCreateSchema`, добавляя дополнительные
    поля, такие как идентификатор, ID пользователя и временные метки.

    Attributes:
        id (int): Уникальный идентификатор неудачи.
        user_id (int): ID пользователя, связанного с неудачей.
        vote (int): Количество голосов (по умолчанию 0).
        created_at (datetime): Дата и время создания записи о неудаче.
        updated_at (datetime): Дата и время последнего обновления записи о неудаче.
        user (UserSchema): Схема пользователя, связанного с неудачей.
    """
    id: int
    user_id: int
    vote: int = 0
    created_at: datetime
    updated_at: datetime
    user: UserSchema