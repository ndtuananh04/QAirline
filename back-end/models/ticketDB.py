from datetime import date
from database import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from models.accountDB import Account
from models.flightDB import Flight
import enum

class TicketClass(enum.Enum):
    ECONOMY = 1
    BUSINESS = 2

class Ticket(db.Model):
    ticket_id = db.Column(db.String(45), primary_key=True, autoincrement=True)
    flight_id = db.Column(db.String(45), db.ForeignKey('flight.flight_id'))
    ticket_number = db.Column(db.String(45), unique=True, nullable=False)
    seat_number = db.Column(db.String(45))
    ticket_class = db.Column(db.Enum(TicketClass), nullable=False)
    booking_time = db.Column(db.DateTime(timezone=True))

    def __init__(self, ticket_id, ticket_number, flight_id, seat_number, ticket_class, booking_time):
        self.ticket_id = ticket_id
        self.ticket_number = ticket_number
        self.flight_id = flight_id
        self.seat_number = seat_number
        self.ticket_class = ticket_class
        self.booking_time = booking_time

    def to_json(self):
        return {
            "ticket_id": self.ticket_id,
            "ticket_number": self.ticket_number,
            "flight_id": self.flight_id,
            "seat_number": self.seat_number,
            "ticket_class": self.ticket_class,
            "booking_time": self.booking_time
        }
    
    @classmethod
    def find_ticket_id(cls, ticket_id):
        return cls.query.filter_by(ticket_id=ticket_id).first()
    
    @classmethod
    def find_flight_id(cls, flight_id):
        return cls.query.filter_by(flight_id=flight_id).first()
    
    @classmethod
    def find_seat_number(cls, seat_number):
        return cls.query.filter_by(seat_number=seat_number).first()
    
    @classmethod
    def find_ticket_number(cls, ticket_number):
        return cls.query.filter_by(ticket_number=ticket_number).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
