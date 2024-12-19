"""
Модуль для определения базовой схемы данных.

Этот модуль содержит класс `BaseSchema`, который наследуется от
`BaseModel` библиотеки Pydantic. Класс предназначен для использования
в других схемах и предоставляет общую конфигурацию для валидации
и сериализации данных.

Класс `BaseSchema` включает в себя настройки, которые позволяют
использовать атрибуты модели в качестве полей схемы.
"""
from typing import TypeVar, Generic, List
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """
    Базовая схема для всех моделей данных.

    Этот класс наследуется от `BaseModel` и предоставляет общую
    конфигурацию для всех схем, включая возможность использования
    атрибутов модели в качестве полей схемы.

    Args:
        model_config (ConfigDict): Конфигурация модели, позволяющая
        использовать атрибуты в качестве полей.
    """
    model_config = ConfigDict(from_attributes=True)
    
T = TypeVar("T", bound=BaseSchema)

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    

class PaginationParams:
    def __init__(
        self,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_desc: bool = True
    ):
        self.skip = skip
        self.limit = limit
        self.sort_by = sort_by 
        self.sort_desc = sort_desc

    @property
    def page(self) -> int:
        return self.skip // self.limit + 1