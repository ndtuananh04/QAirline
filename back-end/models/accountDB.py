from datetime import date
from database import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from models.ticketDB import Ticket
from models.flightDB import Flight
from models.airplaneDB import Airplane
from models.seatsDB import Seats
from models.UserInfoDB import UserInfo
import enum



# Lựa chọn cho tài khoản admin hoăc user
class AccountType(enum.Enum):
    ADMIN = 1
    CUSTOMER = 2

class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), unique=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Enum(AccountType), nullable=False)
    
    def __init__(self, account_id, email, password, role_id):
        self.account_id = account_id
        self.email = email
        self.password = password
        self.role_id = role_id

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

class UserInfo(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accout_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False, onupdate="CASCADE")
    identification = db.Column(db.Integer, unique=True, nullable=False)
    family_name = db.Column(db.String(60), nullable=False)
    given_name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(60), nullable=False)
    nationality = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.DateTime(timezone=True), nullable=False)
    phone_number = db.Column(db.String(45), nullable=False)

    def __init__(self, user_id, identification, family_name, given_name, gender, nationality, date_of_birth, phone_number):
        self.user_id = user_id
        self.identification = identification
        self.family_name = family_name
        self.given_name = given_name
        self.gender = gender
        self.nationality = nationality
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number

    def to_json(self):
        if isinstance(self.date_of_birth, date):
            date_of_birth_json = self.date_of_birth.isoformat()
        else:
            date_of_birth_json = ''
        return {
            "user_id": self.user_id,
            "identification": self.identification,
            "family_name" : self.family_name,
            "given_name": self.given_name,
            "gender": self.gender,
            "nationality": self.nationality,
            "date_of_birth_json": date_of_birth_json,
            "phone_number": self.phone_number
        }
    
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