# Import the Flask package
import flask
from flask import Flask,render_template,redirect,session,send_from_directory,abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os.path
from os import path,urandom,environ,remove
import hashlib
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import flask_login as flog
from sql import models
import psycopg2
from werkzeug import secure_filename
import uuid




# Initialize Flask
app = Flask(__name__)
app_limiter=Limiter(
       app,
       key_func=get_remote_address,
       default_limits=["200 per day","60 per hour"]
)
db=SQLAlchemy(app)
PASSWORD_SALT ='0'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'tif', 'mp4', 'mp3', 'webm', 'mpg' 'mpeg', 'avi', 'wmv', 'mov'])

# Add administrative views here

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/media/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['upload_folder'],
                               filename, as_attachment=True)


@app.route('/media/profile/<path:filename>')
def uploaded_icons(filename):
    return send_from_directory(app.config['upload_icon_folder'],
                               filename,as_attachement=True)


@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'€'):
        return u'{0:.2f}{1}'.format(amount, currency)
    return dict(format_price=format_price)

@app.context_processor
def utility_processor():
    def get_user_photo(username):
        usermodel = db.session.query(
            models.Userextended).get(username)
        return usermodel.icon_photo_path
    return dict(get_user_photo=get_user_photo)



@app.route("/createcontinue",methods=["GET","POST"])
def createcontinue():
       if flask.request.method == "POST" and session['username']:
              firstname = flask.request.values.get('firstname')
              secondname = flask.request.values.get('secondname')
              description = flask.request.values.get('description')
              email = flask.request.values.get('email')
              institution = flask.request.values.get('institution')
              teacher = flask.request.values.get('teacher')
              icon_file = flask.request.files['avatarid']

              #procssing of user input here
              if(teacher == 'True'):
                     teacher = True
              else:
                     teacher = False
              
              icon_file_path = None
              if(icon_file and icon_file.filename != "" and allowed_file(icon_file.filename)):
                     try:
                            filename=uuid.uuid4()
                            filename=filename.hex
                            filename = filename+'.'+icon_file.filename.rsplit('.', 1)[1]
                            icon_file.save(
                                   app.config['upload_icon_folder']+ filename)
                            icon_file_path = app.config['upload_icon_folder'] + \
                                   filename
                     except:
                            return render_template('create-profile-continued.html',error="not allowed file",code=305)
              else:
                     icon_file_path=app.config['icon_file']
              if(firstname == ""):
                     flask.flash('No first name')
                     return render_template("create-profile-continued.html", error="insert first name", code=401)
              #user processing ends here

              usermodel = db.session.query(models.Userextended).get(session["username"])
              if(usermodel is None):
                     return redirect("/",error="fatal error",code=401)
              usermodel.first_name=firstname
              usermodel.second_name=secondname
              usermodel.email=email
              usermodel.user_description=description
              usermodel.icon_photo_path=icon_file_path
              usermodel.institution=institution
              usermodel.teacher=teacher
              db.session.commit()
              return redirect("/",code=200);
       return "NULL"

              

              
def datamodelusers(username,passhash):
       """initialise all tables for user when created"""
       #sensitive commands dont change order
       new_user=models.Users(username,passhash,'0')
       new_user_continued_null=models.Userextended(username,"User")
       db.session.add(new_user)
       db.session.commit()
       db.session.add(new_user_continued_null)
       db.session.commit()



@app.route("/login",methods=["GET","POST"])
@app_limiter.limit("25 per day")
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
@app_limiter.limit("15 per day")
def data():
       if flask.request.method == 'POST':
            username = str(flask.request.values.get('userid'))
            password = str(flask.request.values.get('passid'))
            passhash = str(hashlib.sha256(password.encode()).digest())
            if(username!="" and password!=""):
                   try:
                          assert(not path.exists(f"data/{username}.csv"))
                          datamodelusers(username,passhash)
                          f=open(f"data/{username}.csv","w")
                          f.write(username+",")
                          f.write(passhash+",")
                          f.write("###")     #to end the file end,simply
                          f.close()
                          session["username"]=username
                          return render_template("create-profile-continued.html", code=200)
                   except OSError:
                            return "couldnot create.Temporary error",500
                   except AssertionError:
                            return render_template("create-profile.html",error="Username exists",code=401)
       else:
              return "no credentials recieved",401
       return "NULL"
"""
@app.route("/deleteaccount")
def deleteaccount():
       if(session["username"]):
              os.remove(f"data/{session['username']}.csv")
              userextends = models.Userextended.query.get(session['username'])
              db.session.delete(userextends)
              db.session.commit()
              user = models.Users.query.get(session['username'])
              db.session.delete(user)
              db.session.commit()
              return redirect("/logout")
       return "NULL"
"""


# Run Flask if the __name__ variable is equal to __main__
if __name__ == "__main__":
       app.secret_key = os.urandom(16)
       app.config['SESSION_TYPE'] = 'filesystem'
       app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=31)
       app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:admin@127.0.0.1:5660/covidpro"
       app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
       app.config['upload_icon_folder'] = "media/profile/"
       app.config['icon_file']="media/profile/default_profile.png"
       app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
       app.config['UPLOADED_PHOTOS_DEST'] = "media/profile/"
       app.config['upload_folder']="media/uploads/"
       app.run(debug=True)
