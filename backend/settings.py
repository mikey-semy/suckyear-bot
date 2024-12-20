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

    """
    
    # Определение окружения
    environment: Environment = Field(default=Environment.DEVELOPMENT)
    
    # Базовые настройки
    app_name: str = Field(default="SuckYearBot")
    app_version: str = Field(default="v1")
    app_description: str = Field(default="SuckYearBot - бот, определяющий пользователя года")
    
    # Префикс для роутеров FastAPI
    api_prefix: str = f"/api/{ app_version }"
    
    # Webhook настройки
    webhook_host: HttpUrl = Field(default="http://localhost")
    webhook_port: int = Field(default=8000)
    
    # Токен бота
    bot_token: SecretStr = SecretStr(
        getenv('BOT_TOKEN_DEV' if environment == Environment.DEVELOPMENT else 'BOT_TOKEN')
    )
    
    # Токен для доступа к API
    auth_url: str = "token"
    token_key: SecretStr
    token_type: str = "bearer"
    token_algorithm: str = "HS256"
    token_expire_minutes: int = 60
    
    # База данных
    dsn: PostgresDsn | str =  Field(default="sqlite+aiosqlite:///./test.db")
    
    # Конфигурация Alembic
    alembic_path: str = Field(default="alembic.ini")
    
    # Документация
    docs_access: bool = Field(default=True)

    # CORS настройки
    allow_origins: List[str] = Field(default=["*"])
    allow_credentials: bool = Field(default=True)
    allow_methods: List[str] = Field(default=["*"])
    allow_headers: List[str] = Field(default=["*"])
    
    
    env: str = getenv("ENVIRONMENT", "development")
    print(f"Environment: {env}")
    model_config = SettingsConfigDict(
        env_file=f".env.{env}" if env == "development" else None,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="",
        case_sensitive=False,
        extra="ignore"
    )

settings = Settings()
__all__ = ["Settings", "Environment", "settings"]
