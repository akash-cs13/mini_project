#Used by website to Generate QR code
import datetime
import pyqrcode
import base64
import png


def qr_code_generate(d,h,m):
    current_dt = datetime.datetime.now()
    dt_obj = current_dt + datetime.timedelta(days=int(d), hours= int(h), minutes= int(m))
    str_bytes = str(dt_obj).encode(encoding='ascii')
    encoded_srt = base64.b64encode(str_bytes)
    qr = pyqrcode.create(encoded_srt)
    qr.png('qr_code.png', scale=8)


if __name__ == "__main__":
    print('hi')



