from datetime import date
from database import db
from sqlalchemy.sql import func
import enum

class GenderType(enum.Enum):
    male = "male"
    female = "female"

class UserInfo(db.Model):
    __tablename__ = 'user_info'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id', onupdate="CASCADE", ondelete='CASCADE'), nullable=False)
    identification = db.Column(db.String(20), unique=True, nullable=False)
    family_name = db.Column(db.String(60), nullable=False)
    given_name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.Enum(GenderType), nullable=False)
    nationality = db.Column(db.String(60), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    def __init__(self, account_id, identification, family_name, given_name, gender, nationality, date_of_birth, phone_number):
        self.account_id = account_id
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