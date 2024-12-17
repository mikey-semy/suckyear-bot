# Обработчики команд бота

## Основные команды
- [start](base.py#L21): Начало работы с ботом (/start)
- [help](base.py#L32): Справка (/help)
  

# Обработчики команд c постами

## Создание и управление постами
- [start_fail_creation](fails.py#L32): Начало создания поста (/fail)
- [process_fail_name](fails.py#L58): Обработка ввода названия
- [process_description](fails.py#L89): Обработка ввода описания
- [publish_fail](fails.py#L138): Публикация поста
- [save_draft](fails.py#L178): Сохранение черновика

## Управление черновиками
- [show_drafts](fails.py#L217): Показ списка черновиков (/drafts)
- [manage_draft](fails.py#L258): Меню управления черновиком
- [back_to_drafts](fails.py#L285): Возврат к списку черновиков
- [publish_draft](fails.py#L315): Публикация черновика

## Отмена операций
- [cancel_fail_creation](fails.py#L340): Отмена создания при новой команде
- [cancel_fail_callback](fails.py#L353): Отмена по кнопке
- [cancel_delete](fails.py#L621): Отмена удаления

## Просмотр и голосование
- [show_top_votes](fails.py#L370): Показ топа пользователей (/top)
- [show_fails_for_voting](fails.py#L408): Показ постов для голосования (/vote)
- [read_fail](fails.py#L445): Просмотр поста
- [vote_fail](fails.py#L482): Голосование за пост

## Управление своими постами
- [show_user_fails](fails.py#L532): Показ своих постов (/publics)
- [confirm_delete_fail](fails.py#L558): Подтверждение удаления
- [delete_fail](fails.py#L591): Удаление поста