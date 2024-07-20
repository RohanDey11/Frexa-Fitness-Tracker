from . import db
from flask_login import UserMixin



class Trackers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    tracker_name=db.Column(db.String(100),nullable=False)
    tracker_type=db.Column(db.String(300))
    description=db.Column(db.String(10000))
    settings=db.Column(db.String(1000))


    time_stamp=db.Column(db.DateTime)
    value=db.Column(db.String(100))
    note=db.Column(db.String(10000))

    #associate dif f info foreign keys
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))



class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(150),unique=True)
    password=db.Column(db.String(150))
    first_name=db.Column(db.String(150))

    trackers=db.relationship('Trackers')#list of all trackers user created