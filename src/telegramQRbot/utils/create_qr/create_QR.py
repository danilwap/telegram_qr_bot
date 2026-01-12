import qrcode
import datetime
from logging_config import get_logger
from pathlib import Path

logger = get_logger(__name__)


def create_qr(text: str, size: int, out_path: Path) -> Path:
    start_time = datetime.datetime.now()

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    qr = qrcode.make(text, border=1, box_size=int(size) * 10)
    qr.save(out_path)

    logger.info(
        f"Текст qr: {text}, размер: {size}, path: {out_path} "
        f"Затраченное время: {datetime.datetime.now() - start_time}"
    )
    return out_path
