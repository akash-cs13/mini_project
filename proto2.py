#kind of runs a website
from flask import Flask, render_template, request
import sqlite3
import datetime
import qrcode
import base64




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

@web.route('/login/adduser/',  methods =["GET", "POST"])
def add_user():
    return render_template('add_user.html')




def qr_code_generate(d,h,m):
    current_dt = datetime.datetime.now()
    dt_obj = current_dt + datetime.timedelta(days=d, hours= h, minutes= m)
    str_bytes = str(dt_obj).encode(encoding='ascii')
    encoded_srt = base64.b64encode(str_bytes)
    qr_img = qrcode.make(encoded_srt)
    qr_img.save("images/qr/qr_image.jpg")

def qr_code(days,hours,minutes):
    qr_code_generate(days, hours, minutes)



@web.route('/login/qr-form/',  methods =["GET", "POST"])
def gen_qr():
    if request == "POST":
        days = request.form.get("days")
        hours = request.form.get("hours")
        minutes = request.form.get("minutes")
        qr_code(days,hours,minutes)


    return render_template("qr_generate.html")







#headings = ('Names','Time')
#data = get_log()
#qr_code_generate(0,0,15)
print('done')
web.run(debug=True)
conn.close()