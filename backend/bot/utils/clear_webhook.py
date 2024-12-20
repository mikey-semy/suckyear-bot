from aiogram import Bot
from settings import settings

async def clear():
    bot = Bot(token=settings.bot_token.get_secret_value())
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(clear())