from fastapi import APIRouter
from backend.bot.core.instance import dp, bot

router = APIRouter()

@router.post("/webhook")
async def bot_webhook(update: dict) -> dict:
    """
    Обработчик вебхука для приема обновлений от бота.
    
    :param update: Обновление, полученное от бота.
    """
    await dp.feed_webhook_update(bot, update)
    return {'ok': True}