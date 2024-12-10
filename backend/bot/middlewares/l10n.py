"""
Модуль для определения промежуточного слоя локализации.

Этот модуль содержит класс `L10nMiddleware`, который используется для
добавления объекта локализации в контекст обработки сообщений. Класс
наследуется от `BaseMiddleware` библиотеки aiogram и позволяет
доступ к локализованным строкам в обработчиках сообщений.

Класс `L10nMiddleware` включает в себя методы для инициализации
локализации и обработки входящих сообщений.
"""
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from fluent.runtime import FluentLocalization


class L10nMiddleware(BaseMiddleware):
    """
    Промежуточный слой для локализации сообщений.

    Этот класс добавляет объект локализации в контекст данных,
    доступный в обработчиках сообщений. Это позволяет использовать
    локализованные строки в ответах бота.

    Атрибуты:
        l10n_object (FluentLocalization): Объект локализации для работы с локализованными строками.
    """
    def __init__(self, l10n_object: FluentLocalization):
        """
        Инициализирует промежуточный слой с заданным объектом локализации.

        :param l10n_object: Объект локализации для использования в обработчиках.
        """
        self.l10n_object = l10n_object

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        """
        Обрабатывает входящее сообщение и добавляет объект локализации в контекст.

        :param handler: Обработчик сообщения, который будет вызван.
        :param event: Входящее сообщение.
        :param data: Контекст данных, передаваемый в обработчик.
        
        :return: Результат выполнения обработчика.
        """
        data["l10n"] = self.l10n_object
        await handler(event, data)