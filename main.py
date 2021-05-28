import face_recognition
import numpy as np
import cv2
import os, os.path
import imutils
import base64
import datetime
from dateutil import parser
import time
import keyboard


print('Press \'q\' key to quit anytimeq')
path = os.getcwd()
directory= os.listdir(path+'\\images\\unknown\\')

class Face:

    def __init__(self,known_face_encodings,known_face_names,file_name=''):
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names
        self.file_name = file_name

    # it stores all images and returns boolean value
    def face_det(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        count = 0
        bool = False
        for (x, y, w, h) in faces:
            crop = gray[y:y + h, x:x + w]
            cv2.imwrite(f'images/unknown/frame{count}.jpg', crop)
            count += 1
            bool = True

        return bool

    #takes string of face location and returns name as a string
    def face_rec(self,file_name):
        unknown_image = face_recognition.load_image_file(file_name)

        face_locations = face_recognition.face_locations(unknown_image)
        face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        name = "Unknown"

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
         matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)

         face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
         best_match_index = np.argmin(face_distances)
         if matches[best_match_index]:
             name = self.known_face_names[best_match_index]
        return name

    def qr_det(self,frame):
        bool = False
        d = cv2.QRCodeDetector()
        to_decode, type, pos = d.detectAndDecode(frame)
        base64_bytes = to_decode.encode("ascii")
        decoded_string_bytes = base64.b64decode(base64_bytes)
        decoded_data = decoded_string_bytes.decode("ascii")

        try:
            present = datetime.datetime.now()
            date_time_obj = parser.parse(decoded_data)

            if date_time_obj > present:
                print('unlocking door! with qr')
                bool = True


        except:
            pass

        return bool


def qr_face():
    Door = False
    while (Door == False):

        _, frame = video.read()
        frame = imutils.resize(frame, width=400)

        if face_obj.face_det(frame):
            for unknown_images in directory:
                person_name = face_obj.face_rec('images/unknown/' + unknown_images)

                if person_name != "Unknown":
                    print(f"{person_name} detected")
                    Door = True
                    os.remove(path + '\\images\\unknown\\' + unknown_images)
                    break

        if face_obj.qr_det(frame):
            print('qr code detected')
            Door = True
            break

        if Door == True:
            print('Door is now unlocked for 15s!')
            #time.sleep(15)
            Door = False








face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

print('Face encoding in process....')
face_1 = face_recognition.load_image_file("images/arvind.jpg")
face_1_encoding = face_recognition.face_encodings(face_1)[0]


face_2 = face_recognition.load_image_file("images/gautham.jpg")
face_2_encoding = face_recognition.face_encodings(face_2)[0]
#print(face_2_encoding, '\n', type(face_2_encoding))


face_3 = face_recognition.load_image_file("images/akash.jpg")
face_3_encoding = face_recognition.face_encodings(face_3)[0]
print('Face encoding done!')


face_encoding = [face_1_encoding,face_2_encoding,face_3_encoding]
face_names = ["Arvind","Gautham","Akash"]

face_obj = Face(face_encoding,face_names)

print('Opening Camera.....')
video = cv2.VideoCapture(0)
print('Starting.......')
while True:
    try:
        qr_face()
    except:
        pass

    if keyboard.is_pressed('q'):
        break


video.release()
cv2.destroyAllWindows()


