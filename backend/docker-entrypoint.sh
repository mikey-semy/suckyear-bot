#!/usr/bin/bash

echo "Запуск скрипта docker-entrypoint.sh"

echo "Применение миграции"
poetry run migrate

echo "Запуск API и бота"
poetry run api
