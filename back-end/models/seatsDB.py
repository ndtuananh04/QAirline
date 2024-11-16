from datetime import date
from database import db
from airplaneDB import Airplane
from sqlalchemy.sql import func
import enum

class SeatClass(enum.Enum):
    ECONOMY = 1
    BUSINESS = 2

class Seats(db.Model):
    seat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    airplane_id = db.Column(db.String(60), db.ForeignKey('airplane.airplane_id'), onupdate="CASCADE")
    seat_number = db.Column(db.String(45), nullable=False)
    seat_class = db.Column(db.Enum(SeatClass), nullable=False)
    price = db.Column(db.Decimal(10,2), nullable=False)
    seat_info = db.Column(db.Text, nullable=False)

    def __init__(self, seat_id, seat_number, seat_class, price, seat_info):
        self.seat_id = seat_id
        self.seat_number = seat_number
        self.seat_class = seat_class
        self.price = price
        self.seat_info = seat_info

    def to_json(self):
        return {
            "seat_id": self.seat_id,
            "seat_number": self.seat_number,
            "seat_class": self.seat_class,
            "price": self.price,
            "seat_info": self.seat_info
        }
    
    @classmethod
    def find_seat_id(cls, seat_id):
        return cls.query.filter_by(seat_id=seat_id).first()
    
    @classmethod
    def find_airplane_id(cls, airplane_id):
        return cls.query.filter_by(airplane_id=airplane_id).first()
    
    @classmethod
    def find_seat_number(cls, seat_number):
        return cls.query.filter_by(seat_number=seat_number).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()