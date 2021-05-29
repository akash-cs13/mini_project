# Hosting a website and talking to Database
import cv2
import png
from flask import Flask, render_template, request
from flask import *
from qr_code_generator import qr_code_generate
import sqlite3
import os, os.path
from PIL import Image
from data_base import DataBase



conn = sqlite3.connect('data.db',check_same_thread=False)
cur = conn.cursor()
db_obj = DataBase()
db_obj.create_db()

def pswd(user_name,pswd):

    cur.execute('SELECT * FROM login')
    for a,b in cur.fetchall():
        if user_name == a.rstrip():
            if pswd == b:
                return True
            else:
                return False


web = Flask(__name__)

@web.route('/')
@web.route('/login',  methods =["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("user")
        password = request.form.get("pswd")
        if user_name == 'dsatm' and password == 'dsatm':
            return render_template("admin_log.html",headings=('Names','Time'), data=db_obj.get_log())
        if pswd(user_name,password):
            return render_template("log.html", headings=('Names','Time'), data=db_obj.get_log())
        else:
            return render_template("login_retry.html")
    return render_template("login.html")


path = os.getcwd()
web.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
web.config["IMAGE_UPLOADS"] = path+"\\images\\uploads"

def allowed_image(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in web.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def convert_to_jpg(filename,rename):
    fname = rename.lower()
    img = Image.open(f"images\\uploads\\{filename}")
    img.save(f"images\\{fname}.jpg")
    #img.save(f"images\\{fname}_temp.jpg")
    img.close()



@web.route('/login/adduser',  methods =["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if request.files:
            image = request.files["image"]
            if allowed_image(image.filename):
                filename = image.filename
                rename_filename = name.split()[0]
                image.save(os.path.join(web.config["IMAGE_UPLOADS"], filename))
                convert_to_jpg(filename,rename_filename)
                db_obj.add_to_db(name,password,rename_filename)
                conn.commit()

            else:
                return render_template("user_not_added.html")



            return render_template("user_added.html")
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






if __name__ == "__main__":
    web.run(debug=True)
    conn.close()