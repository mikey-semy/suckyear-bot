from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from shared.models.tags import Tag
from shared.models.post_tags import PostTag
from shared.schemas.tags import TagSchema

from .base import BaseService, BaseDataManager

class TagService(BaseService):
    """
    Сервис для работы с тегами.
    
    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
        
    Methods:
        add_tags: Создает новые теги и возвращает их ID.
        add_post_tags: Создает связи между постами и тегами.
        get_tags_by_post_id: Возвращает теги поста.
    """
    async def add_tags(self, tag_names: list[str]) -> list[int]:
        """
        Создает новые теги в базе данных.

        Args:
            tag_names (list[str]): Список названий тегов

        Returns:
            list[int]: Список ID созданных тегов
        """
        return await TagDataManager(self.session).add_tags(tag_names)

    async def add_post_tags(self, post_tag_pairs: list[dict]) -> None:
        """
        Создает связи между существующими постами и тегами.

        Args:
            post_tag_pairs (list[dict]): Список пар post_id и tag_id
        """
        return await TagDataManager(self.session).add_post_tags(post_tag_pairs)

    async def get_tags_by_post_id(self, post_id: int) -> list[TagSchema]:
        """
        Возвращает все теги поста.

        Args:
            post_id (int): ID поста

        Returns:
            list[TagSchema]: Список тегов поста
        """
        return await TagDataManager(self.session).get_tags_by_post_id(post_id)
    
    async def get_tags_by_ids(self, tag_ids: list[int]) -> list[TagSchema]:
        """
        Возвращает теги по списку их ID.
        
        Args:
            tag_ids (list[int]): Список ID тегов

        Returns:
            list[TagSchema]: Список тегов
        """
        return await TagDataManager(self.session).get_tags_by_ids(tag_ids)


class TagDataManager(BaseDataManager[TagSchema, Tag]):
    """
    Менеджер данных для работы с тегами.
    
    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
        model (Type[Tag]): Модель тега.
        schema (Type[TagSchema]): Схема тега.
    """
    def __init__(self, session: AsyncSession):
        """
        Инициализация менеджера данных для постов.
        """
        super().__init__(
                session=session,
                schema=TagSchema,
                model=Tag
            )
        
    async def add_tags(self, tag_names: list[str]) -> list[int]:
        """
        Добавляет теги в базу данных, если они еще не существуют.
        Возвращает список идентификаторов добавленных тегов.
        
        Args:
            tag_names (list[str]): Список имен тегов.

        Returns:
            list[int]: Список идентификаторов добавленных тегов.
        """
        tag_ids = []
        for tag_name in tag_names:
            tag_name = tag_name.lower()
            statement = select(self.model).filter_by(name=tag_name)
            tag = await self.get_one(statement)

            if tag:
                tag_ids.append(tag.id)
            else:
                new_tag = self.model(name=tag_name)
                created_tag = await self.add_one(new_tag)
                tag_ids.append(created_tag.id)

        return tag_ids

    async def add_post_tags(self, post_tag_pairs: list[dict]) -> None:
        """
        Добавляет пары "пост-тег" в базу данных.
        Если пост или тег не существуют, они будут созданы.

        Args:
            post_tag_pairs (list[dict]): Список словарей, где каждый словарь содержит ключи 'post_id' и 'tag_id'.
        
        Returns:
            None
        """
        # Создаем связи только для существующих постов и тегов
        post_tags = [
            PostTag(post_id=pair_dict['post_id'], tag_id=pair_dict['tag_id'])
            for pair_dict in post_tag_pairs
            if pair_dict['post_id'] and pair_dict['tag_id']
        ]
        # Добавляем связи в базу
        if post_tags:
            for post_tag in post_tags:
                await self.add_one(post_tag)

    async def get_tags_by_post_id(self, post_id: int) -> list[TagSchema]:
        """
        Получает список тегов, связанных с постом.

        Args:
            post_id (int): ID поста.

        Returns:
            list[TagSchema]: Список тегов.
        """
        statement = select(self.model).join(PostTag).filter(PostTag.post_id == post_id)
        return await self.get_all(statement)

    async def get_tags_by_ids(self, tag_ids: list[int]) -> list[TagSchema]:
        """
        Получает список тегов по их идентификаторам.

        Args:
            tag_ids (list[int]): Список идентификаторов тегов.

        Returns:
            list[TagSchema]: Список тегов.
        """
        statement = select(self.model).filter(self.model.id.in_(tag_ids))
        return await self.get_all(statement)