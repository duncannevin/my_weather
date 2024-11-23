from cache.cache import cache
from cache.redis_client import RedisClient
from settings import settings

redis_client = RedisClient(settings.LOCAL_REDIS_HOST)

__all__ = ["cache", "redis_client"]
