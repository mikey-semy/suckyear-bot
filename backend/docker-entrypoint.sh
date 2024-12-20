#!/usr/bin/bash

echo "Запуск скрипта docker-entrypoint.sh"

echo "Установка зависимостей"
poetry install

echo "Применение миграции"
poetry run migrate

echo "Запуск бота"
poetry run api