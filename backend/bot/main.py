import logging
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI

from bot.core.instance import dp, bot
from settings import settings, Environment
from bot.middlewares import L10nMiddleware, UserMiddleware, DatabaseMiddleware
from bot.handlers import all_handlers
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
            health_url = f"{settings.internal_api_url}/health"
            for attempt in range(settings.webhook_setup_retries):
                try:
                    async with bot.session.get(health_url) as response:
                        data = await response.json()
                        if data.get("status") == "ok":
                            webhook_url = f"{settings.webhook_host}/webhook"
                            await bot.set_webhook(
                                url=webhook_url,
                                max_connections=settings.webhook_max_connections,
                                allowed_updates=settings.webhook_allowed_updates,
                                drop_pending_updates=settings.webhook_drop_pending,
                                secret_token=settings.webhook_secret_token.get_secret_value()
                            )
                            logging.info("Webhook запущен: %s", webhook_url)
                            break
                except:
                    pass
                    
                logging.warning(f"API не готов, попытка {attempt + 1} из {settings.webhook_setup_retries}")
                await asyncio.sleep(settings.webhook_retry_delay)
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

async def setup_webhook():
    try:
        webhook_url = f"{settings.webhook_host}/webhook"
        await bot.set_webhook(url=webhook_url)
        logging.info("Webhook запущен: %s", webhook_url)
    except Exception as e:
        logging.error("Ошибка установки вебхука: %s", e)