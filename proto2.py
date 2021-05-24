#Not completed
#sql and web purpose
filehnd = open('known_faces.txt')

for line in filehnd:
    print(line.rstrip())

face_1 = face_recognition.load_image_file("images/veena.jpg")
face_1_encoding = face_recognition.face_encodings(face_1)[0]