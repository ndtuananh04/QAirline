from datetime import date
from database import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from models.ticketDB import Ticket
from models.flightDB import Flight
from models.airplaneDB import Airplane
from models.seatsDB import Seats
import enum


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