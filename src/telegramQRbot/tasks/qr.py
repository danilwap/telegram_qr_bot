# src/telegramQRbot/tasks/qr.py
from telegramQRbot.celery_app import celery_app

@celery_app.task(name="tasks.generate_qr")
def generate_qr(payload: dict) -> str:
    # пока просто проверим, что задача доходит
    return f"got job_id={payload.get('job_id')}"
