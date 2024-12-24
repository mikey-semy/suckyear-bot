"""
Модуль для объединения всех роутеров API v2.

Этот модуль собирает все роутеры из подмодулей:
- <module>: <description>

Экспортирует:
- get_routers(): Функция для получения объединенного роутера
"""
from fastapi import APIRouter
# from . import <module> # TODO: Добавить модули для API v2 в формате module

__all__ = [] # TODO: Добавить модули для API v2 в формате строки "module"

def get_routers() -> APIRouter:
    """
    Функция для получения объединенного роутера.
    
    Returns:
        APIRouter: Объединенный роутер.
    """
    router = APIRouter()
    
    for module in __all__:
        module_router = getattr(globals()[module], "router")
        router.include_router(module_router)
    
    return router