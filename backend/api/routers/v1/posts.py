from typing import List
from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from backend.shared.database.session import get_async_session
from backend.shared.schemas.base import Page, PaginationParams
from backend.shared.schemas.posts import PostSchema, PostCreateSchema, PostStatus
from backend.shared.services.posts import PostService
from backend.shared.exceptions.posts import PostNotFoundError, PostCreateError, PostUpdateError

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostSchema)
async def create_post(
    post: PostCreateSchema,
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> PostSchema:
    """
    Добавляет новый пост.
    
    Args:
        post (PostCreateSchema): Данные нового поста.
        user_id (int): ID пользователя, создавшего пост.
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        PostSchema: Созданный пост.

    Raises:
        HTTPException: Если не удалось создать пост.
    """
    try:
        return PostService(session).create_post(post, user_id)
    except SQLAlchemyError as e:
        raise PostCreateError(str(e)) from e

@router.put("/{post_id}/status", response_model=PostSchema)
async def update_post_status(
    post_id: int,
    status: PostStatus,
    session: AsyncSession = Depends(get_async_session)
) -> PostSchema:
    """
    Обновляет статус поста.

    Args:
        post_id (int): ID поста.
        status (PostStatus): Новый статус поста.
        session (AsyncSession): Асинхронная сессия базы данных.
    Returns:
        PostSchema: Обновленный пост.

    Raises:
        HTTPException: Если не удалось обновить статус поста.
    """
    try:
        updated_post = await PostService(session).update_post_status(post_id, status)
        if not updated_post:
            raise PostNotFoundError(post_id)
        return updated_post
    except SQLAlchemyError as e:
        raise PostUpdateError(post_id, str(e)) from e

@router.get("/{post_id}", response_model=PostSchema)
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> PostSchema:
    """
    Получает пост по его ID.
    
    Args:
        post_id (int): ID поста.
        session (AsyncSession): Асинхронная сессия базы данных.
    
    Returns:
        PostSchema: Найденный пост.
    
    Raises:
        HTTPException: Если пост не найден.
    """
    try:
        post = await PostService(session).get_post(post_id)
        if not post:
            raise PostNotFoundError(post_id)
        return post
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении поста: {str(e)}"
        ) from e

@router.get("/", response_model=Page[PostSchema])
async def get_posts(
    pagination: PaginationParams = Depends(),
    search: str = None,
    status: PostStatus = None,
    tags: List[str] = Query(None),
    user_id: int = None,
    session: AsyncSession = Depends(get_async_session)
) -> Page[PostSchema]:
    """
    Получает список постов с пагинацией, поиском, фильтрацией и сортировкой.

    Args:
        pagination (PaginationParams): Параметры пагинации.
        search (str): Строка поиска.
        status (PostStatus): Статус поста.
        tags (List[str]): Список тегов.
        user_id (int): ID пользователя.
        session (AsyncSession): Асинхронная сессия базы данных.

    Returns:
        Page[PostSchema]: Страница с постами.
    
    Raises:
        HTTPException: Если не удалось получить посты.
    """
    try:
        posts, total = await PostService(session).get_posts(
            pagination=pagination,
            search=search,
            status=status,
            tags=tags,
            user_id=user_id,
        )
        return Page(
            items=posts,
            total=total,
            page=pagination.page,
            size=pagination.limit
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении постов: {str(e)}"
        ) from e