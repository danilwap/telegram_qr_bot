import qrcode
import datetime
from logging_config import get_app_logger

logger = get_app_logger()


def create_qr(text: str, size: str, id: int):
    start_time = datetime.datetime.now()
    qr = qrcode.make(text, border=1, box_size=int(size)*10)
    qr.save(f'result{id}.png')
    logger.info(f'Текст qr: {text}, размер: {size}, id: {id}\nЗатраченное время: {datetime.datetime.now() - start_time}')
    return f'result{id}.png'


