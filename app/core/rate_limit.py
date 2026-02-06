from fastapi import HTTPException, status
from app.core.redis import get_redis


LIKE_LIMIT = 30
LIKE_WINDOW_SECONDS = 60


async def rate_limit_like(user_id: int) -> None:
    redis = get_redis()
    key = f"rate:like:{user_id}"

    count = await redis.incr(key)

    if count == 1:
        await redis.expire(key, LIKE_WINDOW_SECONDS)

    if count > LIKE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many likes. Please try again later.",
        )
