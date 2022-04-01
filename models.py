from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    sex = db.Column(db.String(10))
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    profile = db.Column(db.String(128))
    weight = db.Column(db.Integer)

    access_token = db.Column(db.String(128), unique=True, index=True)
    refresh_token = db.Column(db.String(128), unique=True, index=True)

    # TODO: store as datetime/timestamp?
    expires_at = db.Column(db.String(64))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)