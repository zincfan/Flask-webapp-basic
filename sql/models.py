from flask_hello import db
from sqlalchemy.sql import func

#specific to user view 
class Userprivate(db.Model):
    __tablename__ = 'userprivate'
    username = db.Column(db.String(50),primary_key=True)

    password_hash = db.Column(db.String(), index=False, nullable=False,unique=False)

    password_salt = db.Column(db.String(10),nullable=False)   #not currently use defaults to '0'

    created_on = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    last_password_changed = db.Column(db.DateTime(timezone=True),default=func.now(),nullable=False)

    last_login = db.Column(db.DateTime(timezone=True),default=func.now(),nullable=False)

    def __init__(self, username,password_hash,password_salt):
        self.username=username
        self.password_hash=password_hash
        self.password_salt=password_salt

    def __repr__(self):
        return '<id {}>'.format(self.username)


#specific to public view
class Userpublic(db.Model):
    __tablename__ = 'userpublic'

    username = db.Column(db.String(50),db.ForeignKey('userprivate.username'), primary_key=True,nullable=False)

    first_name = db.Column(db.String(50),nullable=False)

    second_name = db.Column(db.String(40),nullable=True)

    icon_photo_path = db.Column(db.String(70),nullable=False)

    user_description = db.Column(db.String(225),nullable=True)

    email = db.Column(db.String(30),nullable=True)

    last_active = db.Column(db.DateTime(timezone=True),default=func.now(), nullable=False)

    def __init__(self, username,first_name, second_name=None, user_description = None, email = None, icon_photo_path="media/profile/default_profile.png"):
        self.username=username
        self.first_name=first_name
        self.second_name=second_name
        self.user_description = user_description
        self.email = email
        self.icon_photo_path = icon_photo_path
    
    def __repr__(self):
        return '<first name {}>'.format(self.first_name)


class Userpublicvisibility(db.Model):
    __tablename__ ='userpublicvisibility'
    username = db.Column(db.String(50), db.ForeignKey('userprivate.username'), primary_key=True, nullable=False)
    
    def __init__(self,username):
        self.username=username

        

   
