from redis.asyncio import Redis
from app.core.config import settings

_redis: Redis | None = None


async def connect_redis() -> None:
    global _redis

    if _redis is not None:
        return

    _redis = Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
    )

    # checking that Redis is available
    await _redis.ping()


async def close_redis() -> None:
    global _redis

    if _redis is not None:
        await _redis.close()
        _redis = None


def get_redis() -> Redis:
    if _redis is None:
        raise RuntimeError("Redis is not initialized")
    return _redis
