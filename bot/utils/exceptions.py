class BotError(Exception):
    """Базовый класс для всех исключений бота"""
    pass

class ConfigError(BotError):
    """Ошибки конфигурации"""
    pass

class DatabaseError(BotError):
    """Ошибки базы данных"""
    pass

class LocalizationError(BotError):
    """Ошибки локализации"""
    pass

class TelegramError(BotError):
    """Ошибки взаимодействия с Telegram API"""
    pass

class WebhookError(BotError):
    """Ошибки настройки вебхука"""
    pass
