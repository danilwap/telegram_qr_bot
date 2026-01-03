import os
from celery import Celery

celery_app = Celery(
    "telegramqrbot",
    broker=os.getenv("CELERY_BROKER_URL"),
)

# базовые настройки (минимум)
celery_app.conf.update(
    task_default_queue=os.getenv("CELERY_TASK_DEFAULT_QUEUE", "default"),
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Moscow",
    enable_utc=False,

    # важно для надёжности:
    task_acks_late=True,                 # ack после выполнения
    worker_prefetch_multiplier=1,        # чтобы не забирал пачку задач и не “держал”
)

celery_app.autodiscover_tasks(["telegramQRbot.tasks"])
