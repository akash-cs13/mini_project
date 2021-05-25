from flask import Flask, render_template, request




web = Flask(__name__)

@web.route('/',  methods =["GET", "POST"])
def login():
    if request.method == "POST":
        user_name = request.form.get("user")
        password = request.form.get("pswd")
        if (user_name=='dsatm' and password=='dsatm'):
            return render_template("interface.html")
    return render_template("index.html")


#def index():
#   return render_template('index.html')




web.run(debug=True)
