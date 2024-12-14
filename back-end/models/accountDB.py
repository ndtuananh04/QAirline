from datetime import date
from database import db
from sqlalchemy.sql import func
from models.flightsDB import Flights
from models.airplanesDB import Airplanes
from models.seatsDB import Seats
from models.userInfoDB import UserInfo
from sqlalchemy.orm import aliased
import enum

# Lựa chọn cho tài khoản admin hoăc user
class AccountType(enum.Enum):
    admin = "admin"
    customer = "customer"

class Account(db.Model):
    __tablename__ = 'account'
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), unique=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Enum(AccountType), nullable=False)
    user_info = db.relationship('UserInfo', backref='account', uselist=False)  # Quan hệ 1-1 với bảng UserInfo
    
    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role

    def to_json(self):
        return {
            "email" : self.email,
            "password": self.password,
            "role": self.role.name
        }
        
    @staticmethod
    def get_quantity_role():
        admin_count = db.session.query(db.func.count(Account.account_id)).filter(Account.role == 'admin').scalar()
        customer_count = db.session.query(db.func.count(Account.account_id)).filter(Account.role == 'customer').scalar()
        return {'admin': admin_count, 'customer': customer_count}
        
    @classmethod
    def get_all_accounts(cls):
        accounts = db.session.query(
            Account.account_id,
            Account.email,
            Account.role
        ).all()
        account_list = {}
        for account in accounts:
            if account.account_id not in account_list:
                account_list[account.account_id] = {
                    "account_id": account.account_id,
                    "email": account.email,
                    "role": account.role.name
                }

        results = list(account_list.values())
        return results
    
    @classmethod
    def find_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_account_id(cls, account_id):
        return cls.query.filter_by(account_id=account_id).first()

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