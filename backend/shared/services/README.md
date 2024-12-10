# Сервисы бота

## Управление фейлами (fails.py)

### Создание и публикация
- [create_fail](fails.py#L29): Создание нового фейла
- [publish_draft](fails.py#L277): Публикация черновика
- [delete_fail](fails.py#L168): Удаление фейла

### Получение данных
- [get_fail_by_id](fails.py#L128): Получение фейла по ID
- [get_user_fails](fails.py#L146): Получение фейлов пользователя
- [get_user_drafts](fails.py#L256): Получение черновиков пользователя
- [get_fails_for_voting](fails.py#L109): Получение фейлов для голосования
- [get_top_losers](fails.py#L73): Получение топа лузеров

### Голосование
- [check_user_vote](fails.py#L189): Проверка голоса пользователя
- [update_rating](fails.py#L210): Обновление рейтинга фейла

## Управление пользователями (users.py)
- [get_by_chat_id](users.py#L29): Поиск пользователя по chat_id
- [create_user](users.py#L43): Создание нового пользователя
- [get_or_create_user](users.py#L59): Получение или создание пользователя

## Базовый сервис (base.py)
- [BaseService](base.py#L24): Базовый класс для всех сервисов
