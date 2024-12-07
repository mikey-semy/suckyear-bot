"""
Модуль для экспорта схем приложения.

Этот модуль определяет список доступных схем, которые могут быть
использованы в других частях приложения. Схемы включают в себя
схему пользователя и схемы для работы с неудачами.

Экспортируемые классы:
- UserSchema: Схема для представления данных пользователя.
- FailSchema: Схема для представления данных о неудаче.
- FailCreateSchema: Схема для создания новой записи о неудаче.
"""
from bot.schemas.users import UserSchema
from bot.schemas.fails import FailSchema, FailCreateSchema

__all__ = ["UserSchema", "FailSchema", "FailCreateSchema"]