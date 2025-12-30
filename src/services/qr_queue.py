import json, os, time

from infrastructure.redis_client import get_redis

STREAM_KEY = os.getenv("QR_STREAM_KEY", "qr:jobs")

async def enqueue_qr_job(payload: dict) -> str:
    """
        Кладёт задачу в Redis Stream.
        Возвращает stream_id (например "1700000000000-0").
        """
    redis = get_redis()

    # Норм: в стрим кладём одну строку JSON
    payload_json = json.dumps(payload, ensure_ascii=False)

    # MAXLEN ~ ограничивает рост стрима (не строго, но быстро и практично)
    stream_id = await redis.xadd(
        name=STREAM_KEY,
        fields={"payload": payload_json, "ts": str(int(time.time()))},
        maxlen=100_000,
        approximate=True,
    )
    return stream_id