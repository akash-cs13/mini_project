#Main program that has logic for face and qr code detection also talks with DataBase
import face_recognition
import numpy as np
import cv2
import os, os.path
import imutils
import base64
import datetime
from dateutil import parser
import keyboard
import sqlite3
import time
from data_base import DataBase

print('Press \'q\' key to quit anytime')
path = os.getcwd()
directory = os.listdir(path+'\\images\\unknown\\')
conn = sqlite3.connect('data.db',check_same_thread=False)
cur = conn.cursor()
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
global updating_name

class Face():

    def __init__(self, known_face_encodings, known_face_names, file_name=''):
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names
        self.file_name = file_name

    # it stores all images and returns boolean value
    def face_det(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        count = 0
        boolean = False
        for (x, y, w, h) in faces:
            crop = gray[y:y + h, x:x + w]
            cv2.imwrite(f'images/unknown/frame{count}.jpg', crop)
            count += 1
            boolean = True

        return boolean

    #takes string of face location and returns name as a string
    def face_rec(self, file_name):
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



def qr_det(frame):
    bool_val = False
    d = cv2.QRCodeDetector()
    to_decode, _type, pos = d.detectAndDecode(frame)
    base64_bytes = to_decode.encode("ascii")
    decoded_string_bytes = base64.b64decode(base64_bytes)
    decoded_data = decoded_string_bytes.decode("ascii")

    try:
        present = datetime.datetime.now()
        date_time_obj = parser.parse(decoded_data)

        if date_time_obj > present:
            print('valid QR Code is detected')
            bool_val = True
        else:
            print('detected QR Code is expired')
            time.sleep(2)
            os.system('cls')

    except:
        pass

    return bool_val



def qr_face():
    door = False
    while (door == False):

        _, frame = video.read()
        #frame = imutils.resize(frame, width=400)

        bool_val = qr_det(frame)
        if bool_val:
            door = True
            person_name = "QR Code"
            db_obj.update_log(person_name)
            print('Door is now unlocked!')
            time.sleep(5)

        if face_obj.face_det(frame):
            for unknown_images in directory:
                person_name = face_obj.face_rec('images/unknown/' + unknown_images)

                if person_name != "Unknown":
                    print(f"\n\n{person_name} detected")
                    door = True
                    db_obj.update_log(person_name)
                    print('Door is now unlocked for 5s!')
                    time.sleep(5)
                    for images in directory:
                        os.remove(path + '\\images\\unknown\\' + images)
                    time.sleep(3)

                    os.system('cls')
                    break
                else:
                    print('detected person is not in database')


        if door == True:
            #db_obj.update_log(person_name)
            #print('Door is now unlocked for 5s!')
            #time.sleep(5)
            door = False

def face_encode(name_list,image_list):
    print("Face Encoding in Process.......")
    known_face = name_list
    known_image = []
    for image in image_list:
        face = face_recognition.load_image_file(str(image))
        face_encoding = face_recognition.face_encodings(face)[0]
        known_image.append(face_encoding)
    print("Face Encoding done!")
    return [known_face,known_image]


if __name__ == "__main__":

    #Create database if it is not present
    db_obj = DataBase()
    db_obj.create_db()

    #Get names and images to be encoded and initialise
    information_to_encode = db_obj.load_images()
    encoded_list = face_encode(information_to_encode[0],information_to_encode[1])

    #initalising Face class
    face_obj = Face(encoded_list[1],encoded_list[0])

    #Using camera, to use a video change 0 -> string of video file name
    print('Opening Camera.....')
    video = cv2.VideoCapture(0)
    print('Starting.......')
    os.system('cls')
    #logic for detecting face
    while True:
        try:
            door = False
            while (door == False):

                _, frame = video.read()
                # frame = imutils.resize(frame, width=400)

                bool_val = qr_det(frame)
                if bool_val:
                    door = True
                    person_name = "QR Code"
                    db_obj.update_log(person_name)
                    print('Door is now unlocked!')
                    time.sleep(5)

                if face_obj.face_det(frame):
                    for unknown_images in directory:
                        person_name = face_obj.face_rec('images/unknown/' + unknown_images)

                        if person_name != "Unknown":
                            print(f"\n\n{person_name} detected")
                            door = True
                            db_obj.update_log(person_name)
                            print('Door is now unlocked for 5s!')
                            time.sleep(5)
                            for images in directory:
                                os.remove(path + '\\images\\unknown\\' + images)
                            time.sleep(3)

                            os.system('cls')
                            break
                        else:
                            print('detected person is not in database')

                if door == True:
                    # db_obj.update_log(person_name)
                    # print('Door is now unlocked for 5s!')
                    # time.sleep(5)
                    door = False
        except:
            pass

        if keyboard.is_pressed('q'):
            break


    video.release()
    cv2.destroyAllWindows()
    conn.close()




























