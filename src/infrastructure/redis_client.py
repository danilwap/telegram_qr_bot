import os
import redis.asyncio as redis

_redis: redis.Redis | None = None

def get_redis() -> redis.Redis:
    """Возвращает singleton Redis-клиент
    КЛиент создаётся один раз на процесс"""
    global _redis

    if _redis is None:
        redis_url = os.getenv("REDIS_URL")

        if not redis_url:
            raise RuntimeError("REDIS_URL is not set")

        _redis = redis.from_url(
            redis_url,
            decode_responses=True,  # чтобы строки были str, а не bytes

        )
    return _redis