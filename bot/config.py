"""
Модуль для настройки конфигурации приложения с использованием Pydantic.

Этот модуль определяет класс `Settings`, который наследуется от `BaseSettings`
и используется для загрузки конфигурационных параметров из переменных окружения
или файла `.env`. Он обеспечивает типизацию и валидацию настроек.

Класс `Settings` включает в себя параметры, необходимые для работы бота и
подключения к базе данных.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    """
    Класс для хранения конфигурационных параметров приложения.

    Наследуется от `BaseSettings` и загружает параметры из переменных окружения
    или файла `.env`. Обеспечивает типизацию и валидацию настроек.

    Attributes:
        bot_token (SecretStr): Токен бота для доступа к API.
        dsn (str): Строка подключения к базе данных (по умолчанию - SQLite).
    """
    
    bot_token: SecretStr
    dsn: str =  Field(default="sqlite+aiosqlite:///./test.db")
    
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

settings = Settings()
