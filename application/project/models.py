from flask_login import UserMixin
from . import db

# create user model for db creation (noted db was created in terminal not files)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) #unique identity
    email = db.Column(db.String(100), unique=True) #allow change
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))
    

