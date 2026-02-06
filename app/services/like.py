from app.core.rate_limit import rate_limit_like
from app.repositories.like import LikeRepository
from app.core.redis import get_redis


class LikeService:
    def __init__(self, like_repo: LikeRepository):
        self.like_repo = like_repo

    async def toggle_like(self, user_id: int, post_id: int) -> dict:
        # rate limit
        await rate_limit_like(user_id)

        existing_like = await self.like_repo.get_like(user_id, post_id)

        if existing_like:
            await self.like_repo.delete_like(user_id, post_id)
            status = "unliked"
        else:
            await self.like_repo.create_like(user_id, post_id)
            status = "liked"

        count = await self.like_repo.count_likes(post_id)

        # Disabling post list cache
        redis = get_redis()
        keys = await redis.keys("posts:*")
        if keys:
            await redis.delete(*keys)

        return {
            "post_id": post_id,
            "status": status,
            "likes_count": count,
        }
