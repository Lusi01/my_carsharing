from app import db
from datetime import datetime


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_auto = db.Column(db.String(128), nullable=False)
    describe = db.Column(db.String(128), nullable=False)
    rent_price = db.Column(db.Float)
    transmission = db.Column(db.Boolean)
    img_url = db.Column(db.String(128))
    rents = db.relationship('Rent', backref='car', cascade='all,delete-orphan')


class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    created = db.Column(db.DateTime, default=datetime.now)
    completion = db.Column(db.DateTime)






