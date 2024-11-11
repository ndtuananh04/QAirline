from datetime import date
from database import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import enum

class FlightType(enum.Enum):
    SCHEDULED = 1
    DELAYED = 2
    CANCELLED = 3
class Flight(db.Model):
    flight_id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(60), unique=True, nullable=True)
    departure = db.Column(db.String(60), nullable=True)
    arrival = db.Column(db.String(60), nullable=True)
    departure_time = db.Column(db.DateTime(timezone=True), nullable=True)
    arrival_time = db.Column(db.DateTime(timezone=True), nullable=True)
    status = db.Column(db.Enum(FlightType), nullable=True)
    available_seats = db.Column(db.Integer, nullable=True)
    airplane_id = db.Column(db.Integer, db.ForeignKey('airplane.airplane_id'))

    def __init__(self, flight_id, flight_number, departure, arrival, departure_time, arrival_time, flight_type, price, capacity, available_seats):
        self.flight_id = flight_id
        self.flight_number = flight_number
        self.departure = departure
        self.arrival = arrival
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.flight_type = flight_type
        self.price = price
        self.capacity = capacity
        self.available_seats = available_seats

    def to_json(self):
        return {
            "flight_id": self.flight_id,
            "flight_number" : self.flight_number,
            "departure": self.departure,
            "arrival": self.arrival,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "flight_type": self.flight_type,
            "price": self.price,
            "capacity": self.capacity,
            "available_seats": self.available_seats,
        }
    
    @classmethod
    def find_flight_number(cls, flight_number):
        return cls.query.filter_by(flight_number=flight_number).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
