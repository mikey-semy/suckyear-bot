# Бэкэнд (api) SuckYearBot

## Технологии
- Python 3.12
- FastAPI
- SQLAlchemy
- Aiogram 3
- Poetry

## Установка
```bash
cd backend
poetry install
poetry run migrate
poetry run api
poetry run bot
```

## Скрипты

- poetry run api - Запуск API
- poetry run bot - Запуск бота
- poetry run dbinit - Инициализация алембик (ещё не проверял, нужно сделать для асинхронного алембика)
- poetry run makemigrations - Создание миграций 
- poetry run migrate - Миграции
- poetry run rollback - Откат миграций

##  Структура проекта
```
backend/
    ├── api/           # FastAPI сервер
    ├── bot/           # Telegram бот
    └── shared/        # Общий код
```