"""
Модуль для настройки конфигурации приложения с использованием Pydantic.

Этот модуль определяет класс `Settings`, который наследуется от `BaseSettings`
и используется для загрузки конфигурационных параметров из переменных окружения
или файла `.env`. Он обеспечивает типизацию и валидацию настроек.

Класс `Settings` включает в себя параметры, необходимые для работы бота и
подключения к базе данных.
"""
from os import getenv
from typing import List
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, HttpUrl, PostgresDsn


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    
class Settings(BaseSettings):
    """
    Класс для хранения конфигурационных параметров приложения.

    Наследуется от `BaseSettings` и загружает параметры из переменных окружения
    или файла `.env`. Обеспечивает типизацию и валидацию настроек.

    Attributes:
        bot_token (SecretStr): Токен бота для доступа к API.
        dsn (str): Строка подключения к базе данных (по умолчанию - SQLite).
    """
    
    # Определение окружения
    environment: Environment = Field(default=Environment.DEVELOPMENT)
    
    # Базовые настройки
    app_name: str = Field(default="SuckYearBot")
    app_version: str = Field(default="v1")
    app_description: str = Field(default="SuckYearBot - бот, определяющий лоха года")
    
    # Префикс для роутеров FastAPI
    api_prefix: str = f"/api/{ app_version }"
    
    # Webhook настройки
    webhook_host: HttpUrl = Field(default="http://localhost")
    webhook_port: int = Field(default=8000)
    
    bot_token: SecretStr = SecretStr(
        getenv('BOT_TOKEN_DEV' if environment == Environment.DEVELOPMENT else 'BOT_TOKEN')
    )
    
    # База данных
    dsn: PostgresDsn | str =  Field(default="sqlite+aiosqlite:///./test.db")
    
    alembic_path: str = Field(default="backend/alembic.ini")
    
    # Документация
    docs_access: bool = Field(default=True)

    # CORS настройки
    allow_origins: List[str] = Field(default=["*"])
    allow_credentials: bool = Field(default=True)
    allow_methods: List[str] = Field(default=["*"])
    allow_headers: List[str] = Field(default=["*"])
    
    
    env: str = getenv("ENVIRONMENT", "development")
    model_config = SettingsConfigDict(
        #env_file=f".env.{Environment.DEVELOPMENT}",
        env_file=f".env.{env}",
        env_file_encoding="utf-8",
        env_nested_delimiter="__"
    )

settings = Settings()
__all__ = ["Settings", "Environment", "settings"]