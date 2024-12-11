from datetime import date
from database import db
from sqlalchemy.sql import func
import enum
from models.airplanesDB import Airplanes

class SeatClass(enum.Enum):
    ECONOMY = "ECONOMY"
    SKYBOSS = "SKYBOSS"
    BUSINESS = "BUSINESS"

    @classmethod
    def from_string(cls, value):
        try:
            return cls[value.upper()]  # Chuyển giá trị thành chữ hoa trước khi đối chiếu
        except KeyError:
            raise ValueError(f"Invalid flight type: {value}")

class Seats(db.Model):
    __tablename__ = 'seats'
    seat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    airplane_id = db.Column(db.Integer, db.ForeignKey('airplanes.airplane_id'), onupdate="CASCADE")
    seat_number = db.Column(db.String(10), nullable=False)
    seat_class = db.Column(db.Enum(SeatClass), nullable=False)
    price = db.Column(db.Numeric(10, 0), nullable=False)
    seat_info = db.Column(db.Text, nullable=False)

    def __init__(self, airplane_id, seat_number, seat_class, price, seat_info):
        self.airplane_id = airplane_id
        self.seat_number = seat_number
        self.seat_class = SeatClass.from_string(seat_class.upper())
        self.price = price
        self.seat_info = seat_info

    def to_json(self):
        return {
            "airplane_id": self.airplane_id,
            "seat_number": self.seat_number,
            "seat_class": self.seat_class.name,
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