#kind of runs a website
from flask import Flask, render_template, request
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

@web.route('/',  methods =["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("user")
        password = request.form.get("pswd")
        if user_name == 'dsatm' and password == 'dsatm':
            return render_template("admin_log.html")
        if pswd(user_name,password):
            return render_template("log.html", headings=headings, data=data)
        else:
            return render_template("login_retry.html")
    return render_template("login.html")

@web.route('/qr_generate', methods=["GET","POST"])

def open_qr():
    return render_template("qr_geneate.html")


#def index():
#   return render_template('index.html')



headings = ('Names','Time')
data = get_log()
web.run(debug=True)
conn.close()