import sys
import logging
from alembic.config import Config
from alembic import command
from settings import settings

class Migrate:
    """
    Класс для управления миграциями базы данных с использованием Alembic.
    """
    def __init__(self):
        """
        Инициализирует экземпляр класса Migrate.
        """
        self.alembic_cfg = Config(settings.alembic_path)
        
    def initial_migration(self, name_folder: str = "migrations", path_folder: str = "."):
        """
        Инициализирует миграции, создавая папку миграций и файл alembic.ini
        
        #! Требуется создать для асинхронного алембик, так же требуется редактирование параметров в alembic.ini и в env.py
        
        Args:
            name_folder (str, optional): Имя папки для миграций. По умолчанию "migrations".
            path_folder (str, optional): Путь к папке для миграций. По умолчанию ".".
        """
        try:
            command.init(name_folder, path_folder)
            logging.info("Миграции инициализированы")
        except Exception as e:
            logging.error("Ошибка при инициализации миграций: %s", e)
            raise
    
    def create_migration(self, message: str):
        """
        Создает новую миграцию

        Args:
            message (str): Сообщение для миграции
        """
        try:
            command.revision(self.alembic_cfg, autogenerate=True, message=message)
            logging.info("Миграция создана")
        except Exception as e:
            logging.error("Ошибка при создании миграции: %s", e)
            raise
        
    def makemigrations(self):
        """
        Создает миграцию с заданным сообщением
        """
        if len(sys.argv) < 2:
            logging.info("Укажите сообщение для миграции")
            return
        message = sys.argv[1]
        self.create_migration(message)

    def run_migrations(self):
        """
        Применяет все миграции
        """
        try:
            command.upgrade(self.alembic_cfg, "head")
            logging.info("Миграции успешно применены")
        except Exception as e:
            logging.error("Ошибка при применении миграций: %s", e)
            raise

    def rollback_migrations(self):
        """
        Откатывает последнюю миграцию
        """
        try:
            command.downgrade(self.alembic_cfg, "-1")
            logging.info("Откат миграции выполнен")
        except Exception as e:
            logging.error("Ошибка при откате миграции: %s", e)
            raise

def init():
    Migrate().initial_migration()

def makemigrations():
    Migrate().makemigrations()

def migrate():
    Migrate().run_migrations()
    
def rollback():
    Migrate().rollback_migrations()