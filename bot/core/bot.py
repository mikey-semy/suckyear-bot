from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from bot.config import settings

# Инициализация бота с токеном и настройками по умолчанию
bot = Bot(
        # Получение токена бота из настроек
        token=settings.bot_token.get_secret_value(),
        # Установка режима парсинга сообщений
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

# Использование памяти для хранения состояний создания фейлов
storage = MemoryStorage()

# Создание экземпляра диспетчера для обработки обновлений
dp = Dispatcher(storage=storage)
