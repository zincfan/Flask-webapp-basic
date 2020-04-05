# Import the Flask package
import flask
from flask import Flask,render_template,redirect,session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os.path
from os import path
import hashlib


# Initialize Flask
app = Flask(__name__)
app_limiter=Limiter(
       app,
       key_func=get_remote_address,
       default_limits=["200 per day","60 per hour"]
)

# Define the index route
@app.route("/")
def index():
   return render_template("index.html")

@app.route('/favicon.ico')
def logo():
    return redirect('static/icons/favicon.png', code=302)

@app.route("/createpro")
def createpro():
       return render_template("create-profile.html")

@app.route("/test")
def test():
       return render_template("test.html")

@app.route("/seehim")
def seehim():
    return f'''wait until you see him. Oh no no no no oo oo oo ha ha ha - _ - !! <iframe width="560" height="315" src="https://www.youtube.com/embed/7wivOEXlL9s?end=19" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>'''

@app.route("/testmetro")
def testmetro():
       return render_template("testmetro.html")

@app.route("/login",methods=["GET","POST"])
@app_limiter.limit("15 per day")
def login():
       if flask.request.method == "POST":
            username = flask.request.values.get('userid')
            password = flask.request.values.get('passid')
            remme = flask.request.values.get("remme")
            if(username and password):
                   try:
                          assert(path.exists(f"data/{username}.csv"))
                          f = open(f"data/{username}.csv", "r")
                          verihash = f.read().split(',')[1]
                          if(verihash == str(hashlib.sha256(password.encode()).digest())):
                                 session["username"] = username
                                 if(remme==1):
                                     session.permanent = True
                                 return redirect("/",code=302)
                          else:
                                 return render_template("login.html",error="Password doesnot match.",code=401)
                   except OSError:
                            return render_template("login.html", error="Temporary Error.Try later.",code=400)
                   except AssertionError:
                            return render_template("login.html", error="Username doesnot exists.",code=401)
       return render_template("login.html",code=200)

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/',code=302)

@app.route("/data",methods=["GET",'POST'])
def data():
       if flask.request.method == 'POST':
            username = flask.request.values.get('userid') 
            password = flask.request.values.get('passid')
            passhash = str(hashlib.sha256(password.encode()).digest())
            if(username and password):
                   try:
                          assert(not path.exists(f"data/{username}.csv"))
                          f=open(f"data/{username}.csv","w")
                          f.write(username+",")
                          f.write(passhash+",")
                          f.write("###")     #to end the file end,simply
                          f.close()
                          return "created successfully"
                   except OSError:
                            return "couldnot create.Temporary error"
                   except AssertionError:
                            return render_template("create-profile.html",error="Username exists",code=401)
       else:
              return "no credentials recieved"
       return "NULL"




# Run Flask if the __name__ variable is equal to __main__
if __name__ == "__main__":
       app.secret_key = 'superfy6secret_g4ni7key'
       app.config['SESSION_TYPE'] = 'filesystem'
       app.config["PERMANENT_SESSION_LIFETIME"]=31
       app.run(debug=True)
