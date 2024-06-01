from . import db
from flask_login import UserMixin
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_start_h = db.Column(db.Integer)
    time_start_m = db.Column(db.Integer)
    time_end_h = db.Column(db.Integer)
    time_end_m = db.Column(db.Integer)
    weekday = db.Column(db.Integer)
    is_booked = db.Column(db.Boolean)
    is_online = db.Column(db.Boolean)
    is_scanned = db.Column(db.Boolean)
    is_in_progress = db.Column(db.Boolean)
    is_ready = db.Column(db.Boolean)
    is_expired = db.Column(db.Boolean)
    date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    number_of_violations = db.Column(db.Integer, default=0)
    ban_time = db.Column(db.DateTime, default=datetime.now())
    number_booked = db.Column(db.Integer, default=0)
    notes = db.relationship('Note')
    bookings = db.relationship('Booking')
