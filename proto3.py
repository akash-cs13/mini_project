from flask import Flask, render_template, request
import sqlite3
import datetime

conn = sqlite3.connect('data_temp.db',check_same_thread=False)
cur = conn.cursor()


class DataBase:
    def __init__(self):
        pass

    def create_db(self):
        cur.execute('''CREATE TABLE IF NOT EXISTS login( 
        "username" TEXT NOT NULL , 
        "pswd" TEXT NOT NULL  )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS data_main ( 
        "name" TEXT NOT NULL, 
        "img_path" TEXT,  
        "recent_img" TEXT )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS data_time (
        "name" TEXT,
        "time" TEXT )''')
        cur.execute("INSERT INTO login VALUES ('dsatm','dsatm')")
        conn.commit()

    def add_to_db(self,name, pswd, image):
        temp_img = image[:-4] + '_temp.jpg'
        cur.execute(f"INSERT INTO login(username,pswd) VALUES ('{name}','{pswd}')")
        cur.execute(f"INSERT INTO data_main VALUES ('{name}','{image}', '{temp_img}')")
        conn.commit()

    def load_images(self):
        cur.execute('SELECT * FROM data_main')
        names = []
        images = []
        for  name, img, temp_img in cur.fetchall():
            names.append(str(name))
            images.append(str(img))
            names.append(str(name))
            images.append(str(temp_img))
        return [names, images]

    def update_log(self,name):
        cur.execute(f"INSERT INTO data_time VALUES ('{name}','{str(datetime.datetime.now())[:-7]}')")
        conn.commit()

    def get_log(self):
        cur.execute("SELECT * FROM data_time")
        return cur.fetchall()

db = DataBase()
db.create_db()
fhand = open('initial.txt','r')
for line in fhand:
    line = line.rstrip()
    a,b,c = line.split("$")
    db.add_to_db(a,b,c)

def pswd(user_name,pswd):
    cur.execute('SELECT * FROM login')
    for a,b in cur.fetchall():
        if user_name == a:
            if pswd == b:
                return True
            else:
                return False


web = Flask(__name__)

@web.route('/',  methods =["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("user")
        password = request.form.get("pswd")
        if pswd(user_name,password):
            return render_template("interface.html")
    return render_template("login.html")


#def index():
#   return render_template('index.html')




web.run(debug=True)
conn.close()





