"""
Модуль для объединения всех роутеров API v1.

Этот модуль собирает все роутеры из подмодулей:
- posts: Работа с постами
- users: Аутентификация и управление пользователями  
- tags: Управление тегами
- bot: Вебхуки для Telegram бота

Экспортирует:
- get_routers(): Функция для получения объединенного роутера
"""
from fastapi import APIRouter
from . import posts, users, tags, bot

__all__ = ["posts", "users", "tags", "bot"]

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