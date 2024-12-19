from typing import List
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.shared.models.posts import PostModel
from backend.shared.models.tags import TagModel
from backend.shared.models.post_tags import PostTagModel
from backend.shared.schemas.base import PaginationParams
from backend.shared.schemas.posts import PostSchema, PostCreateSchema, PostStatus
from .base import BaseService, BaseDataManager

class PostService(BaseService):
    """
    Сервис для работы с постами.
   
    Args:
        session (AsyncSession): Асинхронная сессия базы данных.
   
    Methods:
        create_post: Создает новый пост в базе данных.
        get_post: Возвращает пост по его идентификатору.
        get_posts: Возвращает список постов с пагинацией, поиском, фильтрацией и сортировкой.
        
        Ещё не реализованы:
        update_post: Обновляет существующий пост.
        delete_post: Удаляет пост из базы данных.
    """

    async def create_post(self, post: PostCreateSchema, user_id: int) -> PostSchema:
        """
        Создает новый пост в базе данных.

        Args:
            post (PostCreateSchema): Данные создаваемого поста
            user_id (int): ID автора поста

        Returns:
            PostSchema: Созданный пост
        """
        return PostDataManager(self.session).create_post(post, user_id)

    async def get_post(self, post_id: int) -> PostSchema:
        """
        Возвращает пост по его ID.

        Args:
            post_id (int): ID запрашиваемого поста

        Returns:
            PostSchema: Найденный пост
        """
        return PostDataManager(self.session).get_post(post_id)

    async def get_posts(
        self,
        pagination: PaginationParams,
        search: str = None,
        status: PostStatus = None,
        tags: List[str] = None,
        user_id: int = None,
    ) -> tuple[List[PostSchema], int]:
        """
        Получает список постов с возможностью пагинации, поиска, фильтрации и сортировки.

        Args:
            pagination (PaginationParams): Параметры пагинации
            search (str): Поиск по названию или контексту поста
            status (PostStatus): Фильтрация по статусу
            tags (List[str]): Фильтрация по тегам
            user_id (int): Фильтрация по пользователю

        Returns:
            tuple[List[PostSchema], int]: Список постов и общее количество
        """
        return PostDataManager(self.session).get_posts(
            pagination=pagination,
            search=search,
            status=status,
            tags=tags,
            user_id=user_id,
        )


class PostDataManager(BaseDataManager[PostSchema]):
    """
    Менеджер данных для работы с постами.

    Args:
        session (AsyncSession): Асинхронная сессия базы данных.  
        schema (Type[PostSchema]): Схема данных поста.
        model (Type[PostModel]): Модель данных поста.
    """
    def __init__(self, session: AsyncSession):
        """
        Инициализация менеджера данных для постов.
        """
        super().__init__(
                session=session, 
                schema=PostSchema, 
                model=PostModel
            )

    async def create_post(self, post: PostCreateSchema, user_id: int) -> PostSchema:
        """
        Создает новый пост в базе данных.

        Args:
            post (PostCreateSchema): Данные создаваемого поста
            user_id (int): ID автора поста

        Returns:
            PostSchema: Созданный пост
        """
        post_data = post.model_dump()
        post_data['user_id'] = user_id
        post_data['status'] = PostStatus.CHECKING
        post_model = PostModel(**post_data)
        return await self.add_one(post_model)
    
    async def get_post(self, post_id: int) -> PostSchema:
        """
        Получает пост по его ID.

        Args:
            post_id (int): ID запрашиваемого поста

        Returns:
            PostSchema: Найденный пост
        """
        statement = select(PostModel).where(PostModel.id == post_id)
        return await self.get_one(statement)

    async def get_posts(
        self,
        pagination: PaginationParams,
        search: str = None,
        status: PostStatus = None,
        tags: List[str] = None,
        user_id: int = None,
    ) -> tuple[List[PostSchema], int]:
        """
        Получает список постов с возможностью пагинации, поиска, фильтрации и сортировки.

        Args:
            pagination (PaginationParams): Параметры пагинации  
            search (str): Поиск по названию или контексту поста
            status (PostStatus): Фильтрация по статусу
            tags (List[str]): Фильтрация по тегам
            user_id (int): Фильтрация по пользователю
            
        Returns:
                tuple[List[PostSchema], int]: Список постов и общее количество
        """
        # Создаем запрос для получения всех постов
        statement = select(PostModel).distinct()

        # Поиск по названию и контенту поста
        if search:
            statement = statement.filter(
                or_(
                    PostModel.name.ilike(f"%{search}%"),
                    PostModel.content.ilike(f"%{search}%")
                )
            )
        
        # Фильтр по статусу
        if status:
            statement = statement.filter(PostModel.status == status)
        
        # Фильтр по тегам
        if tags: 
            statement = statement.join(PostTagModel).join(TagModel).filter(TagModel.name.in_(tags))
            
        # Фильтр по пользователю
        if user_id:
            statement = statement.filter(PostModel.author == user_id)
        
        return await self.get_paginated(statement, pagination)