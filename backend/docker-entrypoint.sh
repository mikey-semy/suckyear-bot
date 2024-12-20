#!/usr/bin/bash

echo "Запуск скрипта docker-entrypoint.sh"

echo "Применение миграции"
poetry run migrate

echo "Запуск сервисов через supervisor"
/usr/sbin/supervisord -c /etc/supervisor/conf.d/supervisord.conf