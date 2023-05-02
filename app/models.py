from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(50), nullable=False)
    pin = db.Column(db.String(4), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)