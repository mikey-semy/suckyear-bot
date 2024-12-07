#!/usr/bin/bash

echo "Запуск скрипта docker-entrypoint.sh"

echo "Применение миграции"
poetry run alembic upgrade head

echo "Запуск бота"
poetry run python -m bot.main