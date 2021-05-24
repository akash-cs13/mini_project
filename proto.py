#to add more faces copy lines 24,25 and rename accordingly
#also add names and encodings to lists in lines 33 & 38
import face_recognition
import numpy as np
import cv2
import os, os.path
import imutils
import base64
import datetime
from dateutil import parser


path = os.getcwd()
directory= os.listdir(path+'\\images\\unknown\\')

#line 17 runs Gauthams video and line 18 runs on webcam
#video = cv2.VideoCapture('vid.mp4')
video = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')

print('Face encoding in process....')

#lines to copy
face_1 = face_recognition.load_image_file("images/arvind.jpg")
face_1_encoding = face_recognition.face_encodings(face_1)[0]

face_2 = face_recognition.load_image_file("images/gau.jpg")
face_2_encoding = face_recognition.face_encodings(face_2)[0]

face_3 = face_recognition.load_image_file("images/akash.jpg")
face_3_encoding = face_recognition.face_encodings(face_3)[0]
#add to lists
known_face_encodings = [
                        face_1_encoding,
                        face_2_encoding,
                        face_3_encoding
]
known_face_names = [
                    "Arvind",
                    "Gautham",
                    "Akash"
]

#takes string of face location and returns name as a string
def face_rec(file_name):
    unknown_image = face_recognition.load_image_file(file_name)
    #unknown_image_to_draw = cv2.imread(file_name)

    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    name = "Unknown"

    for (top,right, bottom, left), face_encoding in zip(face_locations, face_encodings):
      matches = face_recognition.compare_faces(known_face_encodings, face_encoding)


      face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
      best_match_index = np.argmin(face_distances)
      if matches[best_match_index]:
        name = known_face_names[best_match_index]
    #cv2.rectangle(unknown_image_to_draw, (left, top), (right, bottom),(0,255,0),3)
    #cv2.putText(unknown_image_to_draw,name, (left, top-20), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2, cv2.LINE_AA)

    return name

#it stores all images and returns boolean value
def face_det(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    count = 0
    bool=False
    for (x, y, w, h) in faces:
        crop = gray[y:y+h, x:x+w]
        cv2.imwrite(f'images/unknown/frame{count}.jpg',crop)
        count += 1
        bool = True

    return bool

def qr_det(frame):
    bool=False
    d = cv2.QRCodeDetector()
    to_decode,type,pos = d.detectAndDecode(frame)
    base64_bytes = to_decode.encode("ascii")
    decoded_string_bytes = base64.b64decode(base64_bytes)
    decoded_data = decoded_string_bytes.decode("ascii")

    try:
        present = datetime.datetime.now()
        date_time_obj = parser.parse(decoded_data)

        if date_time_obj > present:
            bool = True
            print('Door unlocked!')
    except:
        pass

    return bool

#to remove files in unknown folder
def clear_folder():
    if len(directory)!=0:
        for f in directory:
            os.remove(path+'\\images\\unknown\\'+f)


print('Starting.....')
while True:

    _, frame = video.read()
    frame = imutils.resize(frame, width=400)

    if face_det(frame):
        for unknown_images in directory:
            #print(type(unknown_images),unknown_images)
            person_name = face_rec('images/unknown/'+unknown_images)
            if person_name != "Unknown":
                print(f"Hi {person_name} door is now unlocked!")
                os.remove(path+'\\images\\unknown\\'+unknown_images)
                break

    if qr_det(frame):
        print('qr code detected')
        break




clear_folder()
video.release()
cv2.destroyAllWindows()