from datetime import date
from database import db
from sqlalchemy.sql import func
from models.ticketDB import Ticket
from models.flightDB import Flight
from models.airplaneDB import Airplane
from models.seatsDB import Seats
from models.userInfoDB import UserInfo
import enum

# Lựa chọn cho tài khoản admin hoăc user
class AccountType(enum.Enum):
    admin = 1
    customer = 2

class Account(db.Model):
    __tablename__ = 'account'
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), unique=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Enum(AccountType), nullable=False)
    
    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role

    def to_json(self):
        return {
            "account_id": self.account_id,
            "email" : self.email,
            "password": self.password,
            "role": self.role,
        }
    
    @classmethod
    def find_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_account_id(cls, account_id):
        return cls.query.filter_by(account_id=account_id).first()
    
    @classmethod
    def get_all_ticket(cls, account_id):
        return db.session.query(
                UserInfo.family_name,
                UserInfo.given_name, 
                Ticket.ticket_number, 
                Flight.departure, 
                Flight.arrival, 
                Flight.departure_time, 
                Seats.seat_class
            ) \
            .join(UserInfo, UserInfo.account_id == Account.account_id) \
            .join(Ticket, Ticket.ticket_id == Account.account_id) \
            .join(Flight, Flight.flight_id == Ticket.flight_id) \
            .join(Airplane, Flight.airplane_id == Airplane.airplane_id) \
            .join(Seats, Seats.airplane_id == Airplane.airplane_id) \
            .filter(Account.account_id == account_id) \
            .all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class RevokedTokenModel(db.Model):
    """
    Revoked Token Model Class
    """

    __tablename__ = 'revoked_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    jti = db.Column(db.String(120))

    """
    Save Token in DB
    """

    def add(self):
        db.session.add(self)

        db.session.commit()

    """
    Checking that token is blacklisted
    """

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()

        return bool(query)