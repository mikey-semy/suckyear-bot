# SuckYearBot

## Описание

`SuckYearBot` - это бот, созданный на платформе aiogram, который собирает статистику и показывает рейтинг "пользователей". Рейтинг формируется на основе постов, которые заполняют пользователи и ставят свои оценки. В конце года "пользователем года" становится тот, у кого больше всего постов и самая высокая оценка.

## Установка

Для начала работы с ботом, выполните следующие шаги:

### 1. Клонируйте репозиторий

```bash
mkdir suckyear-bot
cd suckyear-bot
git clone https://github.com/mikey-semy/suckyear-bot.git .
```

### 2. Установите Poetry

Если у вас еще не установлен Poetry, вы можете установить его, следуя [официальной документации](https://python-poetry.org/docs/#installation).

### 3. Установите зависимости

После установки Poetry выполните следующую команду для установки зависимостей:

```bash
poetry install
```

### 4. Настройте переменные окружения

Создайте файл `.env` в корневом каталоге проекта и добавьте следующие переменные:

```
BOT_TOKEN=ваш_токен_бота
DSN=ваш_ссылка_на_базу_данных_postgres (postgresql+asyncpg://username:password@localhost:5432/database_name)_или_sqlite (sqlite+aiosqlite:///./test.db) - sqlite подключен по умолчанию, для тестов на локальном компьютере.
```

### 5. Инициализация базы данных

Для инициализации базы данных выполните следующие команды:

```bash
alembic init migrations
alembic revision --autogenerate -m "Initial"
alembic upgrade head
```

### 6. Запуск бота

Запустите бота с помощью следующей команды:

```bash
poetry run python bot.main
```

## Использование

После запуска бота, пользователи смогут отправлять свои посты и ставить оценки. Бот будет собирать статистику и обновлять рейтинг "пользователей". В конце года будет объявлен "пользователь года".

## Вклад

Если вы хотите внести свой вклад в проект, пожалуйста, создайте форк репозитория и отправьте пулл-реквест с вашими изменениями.

## Лицензия

Этот проект лицензирован под MIT License - смотрите файл [LICENSE](LICENSE) для подробностей.