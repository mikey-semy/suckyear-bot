"""
Основной модуль FastAPI приложения для Telegram бота.

Этот модуль отвечает за:
- Инициализацию FastAPI приложения
    - Настройку веб-хуков для Telegram бота
- Подключение всех необходимых middleware
- Настройку CORS
    - Инициализацию локализации
    - Запуск приложения (dev или prod)

Args:
    app (FastAPI): Основной экземпляр FastAPI приложения
"""
import logging
from socket import gaierror
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.middlewares.docs_blocker import BlockDocsMiddleware
from api.routers import all_routers
from bot.main import lifespan
from settings import settings

# Инициализация приложения FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    lifespan=lifespan
)

# Включение маршрутизаторов для обработки команд и сообщений
app.include_router(all_routers())

# Настройка промежуточных слоев для блокировки доступа к документации
app.add_middleware(BlockDocsMiddleware)

# Настройка промежуточного слоя для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers
)

def run():
    """
    Запуск приложения FastAPI.
    """
    try:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=settings.webhook_port
        )
    except gaierror as e:
        logging.critical("Ошибка сетевого адреса: %s", e)
    except OSError as e:
        logging.critical("Ошибка операционной системы: %s", e)
    except KeyboardInterrupt:
        logging.info("Получен сигнал остановки")
    
if __name__ == "__main__":
    run()
