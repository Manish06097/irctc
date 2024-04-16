# app/models.py

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), nullable=False)

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.String(20), unique=True, nullable=False)
    train_no = db.Column(db.String(20), unique=True, nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    seats_left = db.Column(db.Integer, nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('train.id'), nullable=False)
    no_of_seats_booked = db.Column(db.Integer, nullable=False)
