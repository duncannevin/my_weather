import functools
import json


def get_cached_data(redis_client, cache_key):
    cached_data = redis_client.get(cache_key)
    if cached_data is not None:
        return json.loads(cached_data)
    return cached_data


def set_cached_data(redis_client, cache_key, data):
    redis_client.set(cache_key, json.dumps(data))
    return True


def cache(redis_client):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):  # Handle both args and kwargs

            cache_key = f"{func.__name__}:{kwargs.values()}"
            cached_data = get_cached_data(redis_client, cache_key)

            if cached_data is not None:
                print('Returning cached data:', cached_data)
                return cached_data

            returned_value = await func(*args, **kwargs)
            set_cached_data(redis_client, cache_key, returned_value)
            print('Set cache:', cache_key)
            return returned_value

        return wrapper
    return decorator
