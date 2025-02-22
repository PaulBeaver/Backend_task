from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis


async def init_redis_cache():
    """
    Initializes Redis cache for FastAPI application.

    This function sets up FastAPICache with a Redis backend.

    - Connects to a Redis instance running on localhost.
    - Configures cache encoding and response decoding.
    - Sets cache prefix to 'fastapi-cache'.

    Usage:
        await init_redis_cache()
    """
    redis_client = redis.asyncio.from_url(
        "redis://localhost", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
