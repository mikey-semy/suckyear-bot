"""
Модуль для экспорта схем приложения.

Этот модуль определяет список доступных схем, которые могут быть
использованы в других частях приложения. Схемы включают в себя
схему пользователя и схемы для работы с постами.

Экспортируемые классы:
- UserSchema: Схема для представления данных пользователя.
- PostSchema: Схема для представления данных поста.
- PostCreateSchema: Схема для создания новой записи поста.
"""
from shared.schemas.users import UserSchema
from shared.schemas.posts import PostSchema, PostCreateSchema

__all__ = ["UserSchema", "PostSchema", "PostCreateSchema"]