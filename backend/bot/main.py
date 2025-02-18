import logging

from fastapi import FastAPI
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager


from bot.core.instance import dp, bot
from settings import settings, Environment
from bot.middlewares import L10nMiddleware, UserMiddleware, DatabaseMiddleware
from bot.handlers import all_handlers
from .locales.localization import setup_localization
from .commandsworker import set_bot_commands

async def setup_webhook():
    
    logging.info("Webhook приступает к запуску по адресу: %s", settings.webhook_url)
    
    await bot.set_webhook(
        url=settings.webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    
    logging.info("Webhook запущен: %s", settings.webhook_url)

                    
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
            asyncio.create_task(setup_webhook())
            
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
