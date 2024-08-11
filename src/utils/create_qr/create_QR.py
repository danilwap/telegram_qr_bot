import qrcode



def create_qr(text: str, size: str, id: int):

    qr = qrcode.make(text, border=1, box_size=int(size)*10)
    qr.save(f'result{id}.png')
    return f'result{id}.png'


