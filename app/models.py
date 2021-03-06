from . import db
from werkzeug.security import generate_password_hash
import hashlib

#################################
#Add Location to the profile later
#################################

class UserProfile(db.Model):
    
    __tablename__ = 'users'
    
    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    user_name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(80))
    gender= db.Column(db.String(6))
    email = db.Column(db.String(80))
    role = db.Column(db.String(80))
    isAdmin = db.Column(db.String(6))
    image=db.Column(db.LargeBinary)
    
    def __init__(self, uid, first_name, last_name, user_name, password, gender, email, role, isAdmin, image):
        self.uid=uid
        self.first_name=first_name
        self.last_name=last_name
        self.user_name=user_name
        self.gender=gender
        self.email=email
        self.role=role
        self.isAdmin=isAdmin
        self.image=image
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.uid)  # python 2 support
        except NameError:
            return str(self.uid)  # python 3 support


    def __repr__(self):
        return '<User %r>' % (self.first_name)
