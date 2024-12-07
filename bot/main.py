"""
Модуль main.py содержит основную логику для запуска бота, реализованного с использованием библиотеки aiogram.

Этот модуль отвечает за:
1. Настройку логирования.
2. Загрузку локализации из файлов.
3. Инициализацию бота и диспетчера.
4. Настройку промежуточных слоев для локализации и работы с базой данных.
5. Запуск бота с использованием метода опроса.

Functions:
- main: Основная функция, которая выполняет все шаги по инициализации и запуску бота.
"""
import asyncio
import logging
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fluent.runtime import FluentLocalization, FluentResourceLoader
from .commandsworker import set_bot_commands
from .handlers import setup_routers
from .middlewares.l10n import L10nMiddleware
from .middlewares.user import UserMiddleware
from .middlewares.db import DatabaseMiddleware
from .utils.plural import ru_plural
from .config import settings

async def main():
    """
    Основная функция для инициализации и запуска бота.

    Настраивает логирование, загружает локализацию, инициализирует бота и диспетчер,
    настраивает промежуточные слои и запускает опрос бота.

    Returns:
        None
    """
    
    # Настройка базового конфигурирования логирования
    logging.basicConfig(
            level=logging.INFO, # Уровень логирования #!(можно изменить на DEBUG для более подробной информации)
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", # Формат вывода логов
        )
    
    # Определение пути к папке с локализациями
    locales_path = Path(__file__).parent.joinpath("locales")
    
    # Загрузка ресурсов локализации
    l10n_loader = FluentResourceLoader(str(locales_path) + "/{locale}")
    
    # Инициализация локализации с поддержкой русского языка и файлами локализации
    l10n = FluentLocalization(
            ["ru"], 
            ["strings.ftl", "errors.ftl"],
            l10n_loader,
            functions={'PLURAL': ru_plural}
        )
    
    # Инициализация бота с токеном и настройками по умолчанию
    bot = Bot(
            token=settings.bot_token.get_secret_value(), # Получение токена бота из настроек
            default=DefaultBotProperties(parse_mode=ParseMode.HTML) # Установка режима парсинга сообщений
        )
    
    # Использование памяти для хранения состояний создания фейлов
    storage = MemoryStorage()
    
    # Создание экземпляра диспетчера для обработки обновлений
    dp = Dispatcher(storage=storage)
    
    # Добавление промежуточного слоя для локализации
    dp.update.middleware(L10nMiddleware(l10n))
    
    # Добавление промежуточного слоя для работы с пользователями
    dp.message.middleware(UserMiddleware())
    
    # Добавление промежуточного слоя для работы с базой данных
    dp.update.middleware(DatabaseMiddleware())
    
    # Настройка маршрутизаторов для обработки команд и сообщений
    router = setup_routers()
    dp.include_router(router)
    
    # Установка команд бота с использованием локализации
    await set_bot_commands(bot, l10n)

    # Запуск опроса обновлений от бота
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    # !Можно рассмотреть использование Webhook для улучшения производительности
     
if __name__ == "__main__":
    asyncio.run(main())