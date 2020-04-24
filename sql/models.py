from flask_hello import db
from sqlalchemy.sql import func

#specific to user view 
class Users(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(50),primary_key=True)

    password_hash = db.Column(db.String(), index=False, nullable=False,unique=False)

    password_salt = db.Column(db.String(10),nullable=False)   #not currently in use, defaults to '0'

    created_on = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    last_password_changed = db.Column(db.DateTime(timezone=True),default=func.now(),nullable=False)

    last_login = db.Column(db.DateTime(timezone=True),default=func.now(),nullable=False)

    is_authentic = db.Column(db.Boolean(), nullable=False, default=True)

    def __init__(self, username,password_hash,password_salt):
        self.username=username
        self.password_hash=password_hash
        self.password_salt=password_salt

    def __repr__(self):
        return '<id {}>'.format(self.username)


#specific to public view
class Userextended(db.Model):
    __tablename__ = 'userextended'

    username = db.Column(db.String(50),db.ForeignKey('users.username'), primary_key=True,nullable=False)

    first_name = db.Column(db.String(50),nullable=False)

    second_name = db.Column(db.String(40),nullable=True)

    icon_photo_path = db.Column(db.String(70),nullable=False)

    user_description = db.Column(db.String(225),nullable=True)

    institution = db.Column(db.String(40), nullable=True)

    teacher = db.Column(db.Boolean(),nullable=False,default=False)

    email = db.Column(db.String(30),nullable=True)

    last_active = db.Column(db.DateTime(timezone=True),default=func.now(), nullable=False)

    upload_folder = db.Column(db.String(30),default="media/uploads")

    def __init__(self, username,first_name, second_name=None, user_description = None, email = None, institution= None, teacher =False, icon_photo_path='media/profile/default_profile.png',upload_folder ="media/uploads"):
        self.username=username
        self.first_name=first_name
        self.second_name=second_name
        self.user_description = user_description
        self.email = email
        self.icon_photo_path = icon_photo_path
        self.institution = institution
        self.teacher = teacher
        self.upload_folder = upload_folder
    
    def __repr__(self):
        return '<first name {}>'.format(self.first_name)


        

   
