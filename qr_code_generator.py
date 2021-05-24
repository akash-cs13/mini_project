#Type (days hours minutes) and it generates a qrcode in the folder
#for example if u want to create a qr code which expires in 30 minutes
#give input as 0 0 30
import datetime
import qrcode
import base64


current_dt = datetime.datetime.now()
user_req = list(map(int,input('Enter in format (day hour minute):').split()))
dt_obj = current_dt + datetime.timedelta(days=user_req[0], hours= user_req[1], minutes= user_req[2])
str_bytes = str(dt_obj).encode(encoding='ascii')
encoded_srt = base64.b64encode(str_bytes)
print(dt_obj)
print(encoded_srt)
qr_img = qrcode.make(encoded_srt)
qr_img.save("qr_image.jpg")



