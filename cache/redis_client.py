from typing import Optional, TypeVar

import redis
from redis.client import Redis

T = TypeVar('T')


class RedisClient:
    def __init__(self, url):
        self.url = url
        self.client: Optional[Redis] = None

    def _connect(self):
        if self.client is None:
            self.client = redis.StrictRedis.from_url(
                url=self.url,
            )
        return self.client

    def set(self, key: str, value: T) -> bool:
        self._connect()
        return self.client.set(key, value)

    def get(self, key: str) -> Optional[T]:
        self._connect()
        return self.client.get(key)

    def flushdb(self):
        self._connect()
        return self.client.flushdb()
