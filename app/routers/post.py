from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.post import Post
from app.schemas.post import PostCreate, PostRead
from app.models.user import User

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostRead)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

@router.get("/", response_model=list[PostRead])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return posts
