"""
Модуль для экспорта сервисов приложения.

Этот модуль определяет список доступных сервисов, которые могут быть
использованы в других частях приложения. Сервисы включают в себя
базовый сервис, сервис пользователей и сервис постов.

Экспортируемые классы:
- BaseService: Базовый класс для работы с базой данных.
- UserService: Сервис для работы с пользователями.
- PostService: Сервис для работы с постами.
"""
from backend.shared.services.base import BaseService
from backend.shared.services.users import AuthDataManager as UserService
from backend.shared.services.posts import PostService

__all__ = ["BaseService", "UserService", "PostService"]