from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from bot.settings import settings

# Инициализация бота с токеном и настройками по умолчанию
bot = Bot(
        token=settings.bot_token.get_secret_value(),
        # Установка режима парсинга сообщений
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

# Хранилище состояний
storage = MemoryStorage()

# Инициализация диспетчера
dp = Dispatcher(
    bot=bot, 
    storage=storage
)
