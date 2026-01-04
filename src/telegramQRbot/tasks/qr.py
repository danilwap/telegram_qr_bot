import json
import os
from pathlib import Path
import requests

from telegramQRbot.celery_app import celery_app
from telegramQRbot.utils.create_qr.create_QR import create_qr
from telegramQRbot.keyboards.qr import build_qr_keyboard

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATA_DIR = Path(os.getenv("DATA_DIR", "/docker/telegramqrbot/data"))
API_SEND_PHOTO = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"


def _acquire_lock(lock_path: Path) -> bool:
    # атомарный lock: создаём файл, если его нет
    try:
        fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
        return True
    except FileExistsError:
        return False


def _release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink(missing_ok=True)
    except Exception:
        # не критично: lock может быть очищен вручную/скриптом
        pass


@celery_app.task(
    name="tasks.generate_qr",
    autoretry_for=(requests.RequestException, Exception),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def generate_qr(payload: dict) -> str:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    job_id = payload["job_id"]
    chat_id = str(payload["chat_id"])
    text = payload["qr_text"]
    size = int(payload["qr_size"])

    qrs_dir = DATA_DIR / "qrs"
    qrs_dir.mkdir(parents=True, exist_ok=True)

    out_path = qrs_dir / f"{job_id}.png"
    sent_flag = qrs_dir / f"{job_id}.sent"
    lock_path = qrs_dir / f"{job_id}.lock"

    # 1) если уже отправляли — выходим идемпотентно
    if sent_flag.exists():
        return f"already_sent:{out_path}"

    # 2) lock от гонок
    if not _acquire_lock(lock_path):
        # кто-то уже обрабатывает: лучше retry (задача повторится позже)
        raise RuntimeError("job is locked by another worker")

    try:
        # 3) генерим QR только если файла нет
        if not out_path.exists():
            create_qr(text=text, size=size, out_path=out_path)

        # 4) отправляем с кнопками
        reply_markup = build_qr_keyboard()

        with out_path.open("rb") as f:
            r = requests.post(
                API_SEND_PHOTO,
                data={
                    "chat_id": chat_id,
                    "reply_markup": json.dumps(reply_markup, ensure_ascii=False),
                },
                files={"photo": (out_path.name, f, "image/png")},
                timeout=30,
            )
        r.raise_for_status()

        # 5) помечаем “отправлено” (идемпотентность)
        sent_flag.write_text("1", encoding="utf-8")

        return str(out_path)

    finally:
        _release_lock(lock_path)
