from datetime import date
from database import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import enum


# Lựa chọn cho tài khoản admin hoăc user
class AccountType(enum.Enum):
    ADMIN = 1
    CUSTOMER = 2

class AccountDB(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(60), nullable=True)
    role = db.Column(db.Enum(AccountType), nullable=True)
    is_locked = db.Column(db.Boolean, default=False)
    
    def __init__(self, account_id, email, password, role_id, is_locked):
        self.account_id = account_id
        self.email = email
        self.password = password
        self.role_id = role_id
        self.is_locked = is_locked

    def to_json(self):
        return {
            "account_id": self.account_id,
            "email" : self.email,
            "role": self.role,
            "is_locked": self.is_locked
        }
    
    @classmethod
    def find_email(cls, email, account_id):
        return cls.query.filter_by(email=email, accountId=account_id).first()


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

class UserInfo(db.Model):
    identification = db.Column(db.Integer, db.ForeignKey('account.account_id'), primary_key=True)
    family_name = db.Column(db.String(60), nullable=True)
    given_name = db.Column(db.String(60), nullable=True)
    gender = db.Column(db.String(60), nullable=True)
    nationality = db.Column(db.String(60), nullable=True)
    date_of_birth = db.Column(db.DateTime(timezone=True), nullable=True)
    phone_number = db.Column(db.String(45), nullable=True)

    def __init__(self, identification, family_name, given_name, gender, nationality, date_of_birth, phone_number):
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