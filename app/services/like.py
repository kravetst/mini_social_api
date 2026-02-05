from app.repositories.like import LikeRepository


class LikeService:
    def __init__(self, like_repo: LikeRepository):
        self.like_repo = like_repo

    async def toggle_like(self, user_id: int, post_id: int) -> dict:
        # TODO: додати Redis rate limit
        existing_like = await self.like_repo.get_like(user_id, post_id)
        if existing_like:
            await self.like_repo.delete_like(user_id, post_id)
            status = "unliked"
        else:
            await self.like_repo.create_like(user_id, post_id)
            status = "liked"

        count = await self.like_repo.count_likes(post_id)
        return {"post_id": post_id, "status": status, "likes_count": count}
