from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import PostCreate, PostRead
from app.schemas.user import UserRead
from app.services.post import PostService
from app.services.like import LikeService
from app.repositories.post import PostRepository
from app.repositories.like import LikeRepository
from app.models.user import User
from app.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostRead)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post_service = PostService(PostRepository(db))
    return await post_service.create_post(post.title, post.content, current_user.id)


@router.get("/", response_model=list[PostRead])
async def list_posts(
    db: AsyncSession = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
    author_id: int | None = None,
    search: str | None = None,
    sort: str = "created_at",
    order: str = "desc",
):
    post_service = PostService(PostRepository(db), LikeRepository(db))
    return await post_service.get_posts(limit, offset, author_id, search, sort, order)


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
):
    post_service = PostService(PostRepository(db), LikeRepository(db))
    post = await post_service.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Like/dislike post
@router.post("/{post_id}/like")
async def like_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    like_service = LikeService(LikeRepository(db))
    return await like_service.toggle_like(current_user.id, post_id)
