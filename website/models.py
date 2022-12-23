from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime as dt

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user = db.Column(db.String, db.ForeignKey('user.username'))
    to_user = db.Column(db.String, db.ForeignKey('user.username'))
    message = db.Column(db.String(350), nullable=True)
    photo = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    seen = db.Column(db.Boolean, default=False, nullable=False)
    froms = db.relationship("User", foreign_keys=[from_user])
    tos = db.relationship("User", foreign_keys=[to_user])

    def is_seen(self): 
        return self.seen

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False,)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.String(300), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.Date(), nullable=True)
    country = db.Column(db.String(200), nullable=True)
    state = db.Column(db.String(200), nullable=True)
    profile = db.Column(db.String(500), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    logged = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    def logged_in(self):
        return self.logged