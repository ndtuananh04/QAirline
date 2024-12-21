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
    
class Cancellations(db.Model):
    __tablename__ = 'cancellations'
    cancellation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    cancellation_date = db.Column(db.DateTime, default=func.now())
    
    def __init__(self, ticket_id, reason, cancellation_date):
        self.ticket_id = ticket_id
        self.reason = reason
        self.cancellation_date = cancellation_date
        
    def to_json(self):
        return {
            "ticket_id": self.ticket_id,
            "reason": self.reason,
            "cancellation_date": self.cancellation_date
        }
        
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    

class TicketUser(db.Model):
    __tablename__ = 'ticket_user'
    ticket_user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
    identification = db.Column(db.String(20), unique=True, nullable=False)
    family_name = db.Column(db.String(60), nullable=False)
    given_name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.Enum(GenderTypeTicket), nullable=False)
    nationality = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(60), nullable=False)

    def __init__(self, ticket_id, identification, family_name, given_name, gender, nationality, date_of_birth, phone_number, email):
        self.ticket_id = ticket_id
        self.identification = identification
        self.family_name = family_name
        self.given_name = given_name
        self.gender = gender
        self.nationality = nationality
        self.date_of_birth = date_of_birth
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
            "date_of_birth": self.date_of_birth,
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
    booking_time = db.Column(db.Date, default=func.now())
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
    def find_ticket_number(cls, ticket_number):
        return cls.query.filter_by(ticket_number=ticket_number).first()
    
    @classmethod
    def find_phone_number(cls, ticket_id, phone_number):
        ticket_user = TicketUser.query.filter_by(ticket_id=ticket_id, phone_number=phone_number).first()
        return ticket_user
    
    @classmethod
    def find_seat_number(cls, ticket_id, seat_number):
        ticket = Tickets.query.filter_by(ticket_id=ticket_id, seat_number=seat_number).first()
        return ticket

    # Trả về departure_time để so sánh với current_time
    @classmethod
    def find_departure_time(cls, ticket_id):
        results = db.session.query(
            Flights.departure_time
        ).select_from(Tickets) \
            .join(Flights, Flights.flight_id == Tickets.flight_id) \
            .filter(Tickets.ticket_id == ticket_id) \
            .first()
        return results.departure_time
    
    # Trả về ticket theo flight_id, seat_class, departure_time
    @classmethod
    def get_ticket_admin_dashboard(cls):
        tickets = db.session.query(
            Tickets.ticket_id,
            Tickets.flight_id,
            Tickets.seat_class,
            Flights.departure_time
        ).select_from(Tickets) \
            .join(Flights, Flights.flight_id == Tickets.flight_id) \
            .filter(Tickets.flight_id == Flights.flight_id) \
            .all()
                
        ticket_list = {}
        
        for ticket in tickets:
            if ticket.flight_id not in ticket_list:
                ticket_list[ticket.ticket_id] = {
                    "flight_id": ticket.flight_id,
                    "seat_class": ticket.seat_class.value,
                    "departure_time": ticket.departure_time
                }
            results = list(ticket_list.values())
        return results
    
    # Trả về danh sách vé theo account
    @classmethod
    def get_all_ticket_account_id(cls, account_id):
        tickets = db.session.query(
            Tickets.ticket_id,
            Tickets.ticket_number,
            Tickets.status,
            Tickets.seat_class,
            Tickets.seat_number,
            TicketUser.family_name,
            TicketUser.given_name,
            Flights.departure,
            Flights.code_departure,
            Flights.arrival,
            Flights.code_arrival,
            Flights.departure_time,
            Flights.departure_hour_time,
            Flights.arrival_hour_time,
            Flights.boarding_time,
            Flights.terminal,
        ).select_from(Tickets) \
            .join(Account, Account.account_id == Tickets.account_id) \
            .join(TicketUser, TicketUser.ticket_id == Tickets.ticket_id) \
            .join(Flights, Flights.flight_id == Tickets.flight_id) \
            .filter(Account.account_id == account_id) \
            .all()
        
        print(f"Tickets found: {len(tickets)}")

        ticket_list = {}

        for ticket in tickets:
            if ticket.ticket_number not in ticket_list:
                ticket_list[ticket.ticket_number] = {
                    "ticket_id": ticket.ticket_id,
                    "ticket_number": ticket.ticket_number,
                    "status": ticket.status.value, 
                    "seat_class": ticket.seat_class.value,
                    "seat_number": ticket.seat_number,
                    "family_name": ticket.family_name,
                    "given_name": ticket.given_name,
                    "departure": ticket.departure,
                    "code_departure": ticket.code_departure,
                    "arrival": ticket.arrival,
                    "code_arrival": ticket.code_arrival,
                    "departure_time": ticket.departure_time.strftime('%Y-%m-%d'),
                    "departure_hour_time": ticket.departure_hour_time.strftime('%H:%M'),
                    "arrival_hour_time": ticket.arrival_hour_time.strftime('%H:%M'),
                    "boarding_time": ticket.boarding_time.strftime('%H:%M'),
                    "terminal": ticket.terminal
                }
            results = list(ticket_list.values())
        return results
    
    @classmethod
    def find_flight_id(cls, flight_id):
        return cls.query.filter_by(flight_id=flight_id).first()
    
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


