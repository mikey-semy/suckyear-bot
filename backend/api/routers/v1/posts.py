from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.shared.database.session import get_async_session
from backend.shared.schemas.posts import PostSchema, PostCreateSchema
from backend.shared.services.posts import PostService

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostSchema)
async def create_post(
    post: PostCreateSchema,
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> PostSchema:
    return PostService(session).create_post(post, user_id)

@router.get("/", response_model=PostSchema)
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> PostSchema:
    return PostService(session).get_post(post_id)

@router.get("/", response_model=List[PostSchema])
async def get_posts(
    session: AsyncSession = Depends(get_async_session)
) -> List[PostSchema]:

    return PostService(session).get_posts()