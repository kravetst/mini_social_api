from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import PostCreate, PostRead
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
    like_repo = LikeRepository(db)
    post_service = PostService(PostRepository(db), like_repo)
    return await post_service.get_posts(limit, offset, author_id, search, sort, order)

@router.post("/{post_id}/like")
async def like_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    like_service = LikeService(LikeRepository(db))
    return await like_service.toggle_like(current_user.id, post_id)

