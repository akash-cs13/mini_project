import sqlite3
import face_recognition

conn = sqlite3.connect('data.db')
cur = conn.cursor()


face_1 = face_recognition.load_image_file("images/arvind.jpg")
face_1_encoding = face_recognition.face_encodings(face_1)[0]


class data:
    def __init__(self):
        pass


    #inserting new member, input = ('name','known_image','recent_image')
    def store_to_db(arr):
        cur.execute(f"INSERT INTO known VALUES ('{arr[0]}', '{arr[1]}', '{arr[2]}')")
        conn.commit()

    #removing a colum, input =  string name
    def remove_from_db(str):
        cur.execute(f"DELETE from known WHERE name='{str}'")
        conn.commit()

    def


known_face_encodings = []
known_face_names = []


conn.commit()
conn.close()



