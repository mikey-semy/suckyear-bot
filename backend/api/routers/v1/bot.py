"""
Модуль для обработки вебхуков Telegram бота.

Этот модуль содержит роутер и обработчики для приема и обработки 
вебхук-обновлений от Telegram бота. Используется для интеграции 
бота с веб-сервером через webhook API.

Роутеры:
- /bot/webhook - Эндпоинт для приема вебхуков от Telegram

Зависимости:
- FastAPI для создания API эндпоинтов
- Telegram бот и диспетчер для обработки обновлений
"""
from fastapi import APIRouter
from bot.core.instance import dp, bot

router = APIRouter(prefix="/bot", tags=["Webhook"])

@router.post("/webhook")
async def bot_webhook(update: dict) -> dict:
    """
    Обработчик вебхука для приема обновлений от бота.
    
    Args:
        update (dict): Обновление от бота.

    Returns:
        dict: Результат обработки обновления.
    """
    await dp.feed_webhook_update(bot, update)
    return {'ok': True}
