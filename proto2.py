#kind of runs a website
import cv2
from flask import Flask, render_template, request
from flask import *
from qr_code_generator import qr_code_generate
import sqlite3
import os, os.path


from PIL import Image
path = os.getcwd()
directory= os.listdir(path+'\\images\\unknown\\')
import datetime
import qrcode
import base64
import png



conn = sqlite3.connect('data_temp.db',check_same_thread=False)
cur = conn.cursor()

def pswd(user_name,pswd):

    cur.execute('SELECT * FROM login')
    for a,b in cur.fetchall():
        if user_name == a:
            if pswd == b:
                return True
            else:
                return False

def get_log():
    cur.execute("SELECT * FROM data_time")
    return cur.fetchall()

web = Flask(__name__)

@web.route('/')
@web.route('/login',  methods =["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("user")
        password = request.form.get("pswd")
        if user_name == 'dsatm' and password == 'dsatm':
            return render_template("admin_log.html",headings=('Names','Time'), data=get_log())
        if pswd(user_name,password):
            return render_template("log.html", headings=('Names','Time'), data=get_log())
        else:
            return render_template("login_retry.html")
    return render_template("login.html")


def add_to_db(name, pswd, image):
    temp_img = image[:-4] + '_temp.jpg'
    cur.execute(f"INSERT INTO login(username,pswd) VALUES ('{name}','{pswd}')")
    cur.execute(f"INSERT INTO data_main VALUES ('{name}','{image}', '{temp_img}')")
    conn.commit()



@web.route('/login/adduser',  methods =["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if request.files:
            image = request.files["image"]
            image.save('uploads')


            return render_template("user_add.html")
    return render_template('add_user.html')





@web.route('/login/qr', methods=["GET", "POST"])
def qr_form():
    return render_template("qr_generate.html")


@web.route('/login/qr-form',  methods =["POST"])
def gen_qr():

    days = request.form.get("days")
    hours = request.form.get("hours")
    minutes = request.form.get("minutes")
    qr_code_generate(days, hours, minutes)
    return send_file('qr_code.png', as_attachment=True)


#@web.route('/login/download')
#def qr_code_download():
#    return send_file('qr_code.png', as_attachment=True)




if __name__ == "__main__":
    #headings = ('Names','Time')
    #data = get_log()
    #qr_code_generate(0,0,15)
    web.run(debug=True)
    conn.close()