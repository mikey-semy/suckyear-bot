import logging
from socket import gaierror
import uvicorn
from fastapi import FastAPI
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

async def setup_webhook():
    health_url = f"{settings.internal_api_url}/health"
    logging.info("Проверка доступности API по адресу: %s", health_url)
    while True:
        try:
            async with bot.session.get(health_url) as response:
                data = await response.json()
                logging.info("Статус: %s", data.get("status"))
                if data.get("status") == "ok":
                    webhook_url = f"{settings.webhook_host}/webhook"
                    logging.info("API запущен: %s", health_url)
                    logging.info("Webhook приступает к запуску по адресу: %s", webhook_url)
                    await bot.set_webhook(
                        url=webhook_url,
                        max_connections=settings.webhook_max_connections,
                        allowed_updates=settings.webhook_allowed_updates,
                        drop_pending_updates=settings.webhook_drop_pending,
                        secret_token=settings.webhook_secret_token.get_secret_value()
                    )
                    logging.info("Webhook запущен: %s", webhook_url)
                    return
        except:
            await asyncio.sleep(settings.webhook_retry_delay)
            logging.info("Ожидание готовности API...")

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

app = FastAPI(lifespan=lifespan)

def run():
    """
    Запуск бота с FastAPI.
    """
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=settings.bot_port
        )
    except gaierror as e:
        logging.critical("Ошибка сетевого адреса: %s", e)
    except OSError as e:
        logging.critical("Ошибка операционной системы: %s", e)
    except KeyboardInterrupt:
        logging.info("Получен сигнал остановки")

if __name__ == "__main__":
    run()