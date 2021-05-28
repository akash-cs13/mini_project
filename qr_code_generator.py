#Type (days hours minutes) and it generates a qrcode in the folder
#for example if u want to create a qr code which expires in 30 minutes
#give input as 0 0 30
import datetime

import cv2
import pyqrcode
import qrcode
import base64
import png


def qr_code_generate(d,h,m):
    current_dt = datetime.datetime.now()
    dt_obj = current_dt + datetime.timedelta(days=int(d), hours= int(h), minutes= int(m))
    str_bytes = str(dt_obj).encode(encoding='ascii')
    encoded_srt = base64.b64encode(str_bytes)
    qr = pyqrcode.create(encoded_srt)
    qr.png('qr_code.png', scale=8)
    #qr_img = qrcode.makescale(encoded_srt)
    #return qr_img
    #print(type(qr_img))
    #print(qr_img)
    #qr_img.save("images/qr/qr_image.jpg")



    #cv2.imwrite("images/qr/cv_qr_image.jpg",)


if __name__ == "__main__":
    print('hi')
    #d,h,m = list(map(int,input('Enter in format (day hour minute):').split()))
    #qr_code_generate(0,0,2)
    #while True:
    #    print('_')


