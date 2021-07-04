#To store and display data in Database
import sqlite3
import datetime

conn = sqlite3.connect('data.db',check_same_thread=False)
cur = conn.cursor()


class DataBase:
    def __init__(self):
        pass

    def create_db(self):
        cur.execute('''CREATE TABLE IF NOT EXISTS login( 
        "username" TEXT NOT NULL UNIQUE, 
        "pswd" TEXT NOT NULL  )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS data_main ( 
        "name" TEXT NOT NULL UNIQUE, 
        "img_path" TEXT )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS data_time (
        "name" TEXT,
        "time" TEXT )''')
        try:
            cur.execute("INSERT INTO login VALUES ('dsatm','dsatm')")
        except:
            pass
        conn.commit()

    def add_to_db(self,name, pswd, image):
        cur.execute(f"INSERT INTO login(username,pswd) VALUES ('{name}','{pswd}')")
        cur.execute(f"INSERT INTO data_main VALUES ('{name}','images/{image.lower()}.jpg')")
        conn.commit()

    def load_images(self):
        cur.execute('SELECT * FROM data_main')
        names = []
        images = []
        for  name, img in cur.fetchall():
            names.append(str(name))
            images.append(str(img))
        conn.commit()
        return [names, images]

    def update_log(self,name):
        cur.execute(f"INSERT INTO data_time VALUES ('{name}','{str(datetime.datetime.now())[:-7]}')")
        conn.commit()

    def get_log(self):
        cur.execute("SELECT * FROM data_time")
        temp_list = cur.fetchall()
        return temp_list[::-1]


if __name__ == "__main__":
    db = DataBase()
    db.create_db()
    fhand = open('initial.txt','r')
    for line in fhand:
        line = line.rstrip()
        a,b,c = line.split("$")
        db.add_to_db(a,b,c)
    print(db.load_images())



