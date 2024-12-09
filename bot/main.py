"""
Основной модуль FastAPI приложения для Telegram бота.

Этот модуль отвечает за:
- Инициализацию FastAPI приложения
- Настройку веб-хуков для Telegram бота
- Подключение всех необходимых middleware
- Настройку CORS
- Инициализацию локализации
- Запуск приложения (dev или prod)

Attributes:
    app (FastAPI): Основной экземпляр FastAPI приложения
"""
import asyncio
import logging
from socket import gaierror
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fluent.runtime import FluentLocalization, FluentResourceLoader
from aiogram.exceptions import TelegramAPIError
from .core.instance import bot, dp
from .commandsworker import set_bot_commands
from .handlers import all_handlers
from .routers import all_routers
from .middlewares.l10n import L10nMiddleware
from .middlewares.user import UserMiddleware
from .middlewares.db import DatabaseMiddleware
from .middlewares.docs_blocker import BlockDocsMiddleware
from .utils.plural import ru_plural
from .settings import settings, Environment


@asynccontextmanager
async def lifespan(_application: FastAPI):
    """
    Контекст-менеджер жизненного цикла приложения.
    
    Выполняет инициализацию при запуске и очистку при остановке:
    - Настраивает логирование
    - Инициализирует локализацию
    - Подключает middleware
    - Устанавливает веб-хук для бота
    - При завершении удаляет веб-хук и закрывает сессию
    
    Attributes:
        application (FastAPI): Экземпляр FastAPI приложения
        
    Yields:
        None
    """
    try:
        # Настройка базового конфигурирования логирования
        logging.basicConfig(
                level=logging.INFO, # Уровень логирования
                format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", # Формат вывода логов
            )

        # Инициализация локализации
        try:
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
        except (FileNotFoundError, ValueError) as e:
            logging.error("Ошибка загрузки файлов локализации: %s", e)
            raise
        except ImportError as e:
            logging.error("Ошибка импорта модуля локализации: %s", e)
            raise
        
        # Подключение middleware и handlers
        try:  
            # Добавление промежуточного слоя для локализации
            dp.update.middleware(L10nMiddleware(l10n))

            # Добавление промежуточного слоя для работы с пользователями
            dp.message.middleware(UserMiddleware())

            # Добавление промежуточного слоя для работы с базой данных
            dp.update.middleware(DatabaseMiddleware())

            # Настройка маршрутизаторов для обработки команд и сообщений
            dp.include_router(all_handlers())

            # Установка команд бота с использованием локализации
            await set_bot_commands(bot, l10n)
        except (AttributeError, TypeError) as e:
            logging.error("Ошибка конфигурации middleware или handlers: %s", e)
            raise
            
        # Запуск бота
        try:  
            if settings.environment == Environment.DEVELOPMENT:
                # В development используем polling
                logging.info("Использование polling для разработки")
                asyncio.create_task(
                    dp.start_polling(bot, polling_timeout=30)
                )
                logging.info("Polling started")
            else:
                logging.info("Запуск webhook")
                webhook_url = f"{settings.webhook_host}/webhook"
                await bot.set_webhook(url=webhook_url)
                logging.info("Webhook запущен по адресу %s", webhook_url)
        except (ConnectionError, TimeoutError) as e:
            logging.error("Ошибка сетевого подключения: %s", e)
            raise
        except TelegramAPIError as e:
            logging.error("Ошибка Telegram API: %s", e)
            raise

        yield
        
    except (KeyboardInterrupt, SystemExit):
        logging.info("Получен сигнал остановки")
        raise
    except Exception as e:
        logging.critical("Необработанная ошибка: %s", e)
        raise
    finally:
        try:
            # Остановка бота при завершении работы приложения
            await bot.delete_webhook(drop_pending_updates=True)
            await bot.session.close()
            logging.info("Бот остановлен")
        except (ConnectionError, TimeoutError) as e:
            logging.error("Ошибка при остановке бота: %s", e)

# Инициализация приложения FastAPI
application = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    lifespan=lifespan
)

# Включение маршрутизаторов для обработки команд и сообщений
application.include_router(all_routers())

# Настройка промежуточных слоев для блокировки доступа к документации
application.add_middleware(BlockDocsMiddleware)

# Настройка промежуточного слоя для CORS
application.add_middleware(CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers
)

if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run(
            application,
            host="0.0.0.0",
            port=settings.webhook_port
        )
    except gaierror as e:
        logging.critical("Ошибка сетевого адреса: %s", e)
    except OSError as e:
        logging.critical("Ошибка операционной системы: %s", e)
    except KeyboardInterrupt:
        logging.info("Получен сигнал остановки")
