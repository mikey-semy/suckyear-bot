import logging
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.bot.core.instance import dp, bot
from backend.settings import settings, Environment
from backend.bot.middlewares import L10nMiddleware, UserMiddleware, DatabaseMiddleware
from backend.bot.handlers import all_handlers
from .locales.localization import setup_localization
from .commandsworker import set_bot_commands


@asynccontextmanager
async def lifespan(_app: FastAPI):
    try:
        # Настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        
        # Установка локализации
        l10n = setup_localization(Path(__file__).parent)
     
        # Подключение промежуточных слоев
        dp.update.middleware(L10nMiddleware(l10n))
        dp.message.middleware(UserMiddleware())
        dp.update.middleware(DatabaseMiddleware())

        # Подключение хендлеров
        dp.include_router(all_handlers())

        # Установка команд
        await set_bot_commands(bot, l10n)
      
        # Запуск бота
        if settings.environment == Environment.DEVELOPMENT:
            asyncio.create_task(dp.start_polling(bot, polling_timeout=30))
            logging.info("Polling started")
        else:
            webhook_url = f"{settings.webhook_host}/webhook"
            await bot.set_webhook(url=webhook_url)
            logging.info("Webhook запущен: %s", webhook_url)

        yield
        
    except Exception as e:
        logging.critical("Критическая ошибка: %s", e)
        raise
    finally:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await bot.session.close()
            logging.info("Бот остановлен")
        except Exception as e:
            logging.error("Ошибка остановки бота: %s", e)
