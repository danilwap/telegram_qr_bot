import qrcode
import datetime


def create_qr(text: str, size: str, id: int):
    start_time = datetime.datetime.now()
    qr = qrcode.make(text, border=1, box_size=int(size)*10)
    qr.save(f'result{id}.png')
    print('Затраченное время:', datetime.datetime.now() - start_time)
    return f'result{id}.png'


