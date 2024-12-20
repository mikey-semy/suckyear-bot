import logging
from fastapi import APIRouter
from bot.core.instance import dp, bot

router = APIRouter()

@router.post("/webhook")
async def bot_webhook(update: dict) -> dict:
    """
    Обработчик вебхука для приема обновлений от бота.
    
    Args:
        update (dict): Обновление от бота.

    Returns:
        dict: Результат обработки обновления.
    """
    logging.info(f"Обновления от бота: {update}")
    await dp.feed_webhook_update(bot, update)
    return {'ok': True}