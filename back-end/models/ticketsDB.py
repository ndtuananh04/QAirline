from datetime import date
from database import db
from sqlalchemy.sql import func
import enum
from models.accountDB import Account
from models.flightsDB import Flights
from models.airplanesDB import Airplanes    

class StatusClass(enum.Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"

class GenderTypeTicket(enum.Enum):
    male = "male"
    female = "female"

class SeatClass(enum.Enum):
    economy = "economy"
    business = "business"
    skyboss = "skyboss"

class TicketUser(db.Model):
    __tablename__ = 'ticket_user'
    ticket_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
    identification = db.Column(db.String(20), unique=True, nullable=False)
    family_name = db.Column(db.String(60), nullable=False)
    given_name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.Enum(GenderTypeTicket), nullable=False)
    nationality = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False)

    def __init__(self, ticket_id, identification, family_name, given_name, gender, nationality, phone_number, email):
        self.ticket_id = ticket_id
        self.identification = identification
        self.family_name = family_name
        self.given_name = given_name
        self.gender = gender
        self.nationality = nationality
        self.phone_number = phone_number
        self.email = email

    def to_json(self):
        return {
            "ticket_id": self.ticket_id,
            "identification": self.identification,
            "family_name": self.family_name,
            "given_name": self.given_name,
            "gender": self.gender,
            "nationality": self.nationality,
            "phone_number": self.phone_number,
            "email": self.email
        }
    
    @classmethod
    def find_ticket_user_id(cls, ticket_user_id):
        return cls.query.filter_by(ticket_user_id=ticket_user_id).first()
    
    @classmethod
    def find_ticket_id(cls, ticket_id):
        return cls.query.filter_by(ticket_id=ticket_id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class Tickets(db.Model):
    __tablename__ = 'tickets'
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id'), nullable=False)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False)
    seat_class = db.Column(db.Enum(SeatClass), nullable=False)
    seat_number = db.Column(db.String(10), nullable=True)
    booking_time = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.Enum(StatusClass), nullable=False)

    def __init__(self, account_id, flight_id, ticket_number, seat_class, seat_number, booking_time, status):
        self.account_id = account_id
        self.flight_id = flight_id
        self.ticket_number = ticket_number
        self.seat_class = seat_class
        self.seat_number = seat_number
        self.booking_time = booking_time
        self.status = status

    def to_json(self):
        return {
            "ticket_id": self.ticket_id,
            "flight_id": self.flight_id,
            "ticket_number": self.ticket_number,
            "seat_class": self.seat_class.value,
            "seat_number": self.seat_number,
            "booking_time": self.booking_time,
            "status": self.status.value
        }
    
    @classmethod
    def find_ticket_id(cls, ticket_id):
        return cls.query.filter_by(ticket_id=ticket_id).first()
    
    @classmethod
    def get_all_ticket_account_id(cls, account_id):
        tickets = db.session.query(
            Tickets.ticket_number,
            Tickets.status,
            Tickets.seat_class,
            TicketUser.family_name,
            TicketUser.given_name,
            TicketUser.nationality,
            Flights.departure,
            Flights.arrival,
            Flights.departure_time,
            Flights.departure_hour_time,
        ).select_from(Tickets) \
            .join(Account, Account.account_id == Tickets.account_id) \
            .join(TicketUser, TicketUser.ticket_id == Tickets.ticket_id) \
            .join(Flights, Flights.flight_id == Tickets.flight_id) \
            .filter(Account.account_id == account_id) \
            .all()
        
        print(f"Tickets found: {len(tickets)}")

        results = []

        for ticket in tickets:
            results.append({
                "ticket_number": ticket.ticket_number,
                "status": ticket.status.value, 
                "seat_class": ticket.seat_class.value,
                "family_name": ticket.family_name,
                "given_name": ticket.given_name,
                "nationality": ticket.nationality,
                "departure": ticket.departure,
                "arrival": ticket.arrival,
                "departure_time": ticket.departure_time.strftime('%Y-%m-%d'),
                "departure_hour_time": ticket.departure_hour_time.strftime('%H:%M'),
            })

        return results
    
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


