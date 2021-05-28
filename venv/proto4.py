from flask import *
import sqlite3

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

@web.route('/login/qr',  methods =["GET", "POST"])
def gen_qr():
    return render_template('qr_generate.html')













web.run(debug=True)
conn.close()


