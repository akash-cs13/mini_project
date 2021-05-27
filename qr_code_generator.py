#Type (days hours minutes) and it generates a qrcode in the folder
#for example if u want to create a qr code which expires in 30 minutes
#give input as 0 0 30
import datetime
import qrcode
import base64


def qr_code_generate(d,h,m):
    current_dt = datetime.datetime.now()
    dt_obj = current_dt + datetime.timedelta(days=d, hours= h, minutes= m)
    str_bytes = str(dt_obj).encode(encoding='ascii')
    encoded_srt = base64.b64encode(str_bytes)
    qr_img = qrcode.make(encoded_srt)
    qr_img.save("images/qr/qr_image.jpg")


#d,h,m = list(map(int,input('Enter in format (day hour minute):').split()))
qr_code_generate(0,0,2)

