"""
Модуль для определения схемы пользователя.

Этот модуль содержит класс `UserSchema`, который используется для
валидации и сериализации данных пользователя. Класс наследуется от
`BaseSchema` и определяет структуру данных, связанных с пользователем.

Класс `UserSchema` включает в себя поля, необходимые для представления
пользователя в системе.
"""
from enum import Enum
from datetime import datetime
from backend.shared.schemas.base import BaseSchema

class UserRole(str, Enum):
    """
    Роли пользователя в системе.
    
    Args:
        ADMIN (str): Роль администратора.
        MODERATOR (str): Роль модератора.
        USER (str): Роль пользователя.
    """
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

class CreateUserSchema(BaseSchema):
    """
    Схема для создания пользователя.

    Этот класс используется для валидации и сериализации данных, 
    связанныхс созданием пользователя. 
    
    Args:
        username (str): Имя пользователя.
        chat_id (int): ID чата пользователя. Для регистрации через бота.
        email (str): Электронная почта пользователя. Для регистрации через сайт.
        password (str): Пароль пользователя. Для регистрации через сайт.
    """
    username: str
    chat_id: int | None = None
    email: str | None = None
    password: str | None = None

class UserSchema(BaseSchema):
    """
    Схема для представления данных пользователя.

    Этот класс определяет структуру данных, связанных с пользователем,
    включая его идентификатор, ID чата, имя пользователя и дату создания.

    Args:
        id (int | None): Уникальный идентификатор пользователя (по умолчанию None).
        chat_id (int): ID чата пользователя.
        username (str): Имя пользователя.
        role (UserRole): Роль пользователя.
        created_at (datetime | None): Дата и время создания пользователя (по умолчанию None).
    """
    id: int | None = None
    username: str
    chat_id: int | None
    email: str | None
    role: UserRole = UserRole.USER
    created_at: datetime | None = None
    
class TokenSchema(BaseSchema):
    """
    Токен доступа пользователя.
    
    Args:
        access_token (str): Токен доступа пользователя.
        token_type (str): Тип токена.
    """
    access_token: str
    token_type: str
