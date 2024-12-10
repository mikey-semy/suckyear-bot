"""
Модуль для экспорта сервисов приложения.

Этот модуль определяет список доступных сервисов, которые могут быть
использованы в других частях приложения. Сервисы включают в себя
базовый сервис, сервис пользователей и сервис неудач.

Экспортируемые классы:
- BaseService: Базовый класс для работы с базой данных.
- UserService: Сервис для работы с пользователями.
- FailService: Сервис для работы с неудачами.
"""
from backend.shared.services.base import BaseService
from backend.shared.services.users import UserService
from backend.shared.services.fails import FailService

__all__ = ["BaseService", "UserService", "FailService"]