import redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


async def init_redis_cache():
    redis_client = redis.asyncio.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
