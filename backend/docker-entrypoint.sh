#!/usr/bin/bash

echo "Запуск скрипта docker-entrypoint.sh"

echo "Применение миграции"
poetry run migrate

echo "Запуск апи"
poetry run api

echo "Запуск бота"
poetry run bot