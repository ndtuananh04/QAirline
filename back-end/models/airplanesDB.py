from datetime import date
from database import db
from sqlalchemy.sql import func

class Airplanes(db.Model):
    __tablename__ = 'airplanes'
    airplane_id = db.Column(db.Integer, primary_key=True)
    name_airplane = db.Column(db.String(45), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_locked = db.Column(db.Boolean, default=False)

    def __init__(self, name_airplane, capacity, is_locked):
        self.name_airplane = name_airplane
        self.capacity = capacity
        self.is_locked = is_locked

    def to_json(self):
        return {
            "name_airplane": self.name_airplane,
            "capacity": self.capacity,
            "is_locked": self.is_locked
        }
    
    # Lọc chỉ những airplane chưa khóa
    @classmethod
    def get_all_airplanes(cls):
        airplanes = cls.query.filter_by(is_locked=False).all()
        return [airplane.to_json() for airplane in airplanes]
    
    @classmethod
    def find_airplane_id(cls, airplane_id):
        return cls.query.filter_by(airplane_id=airplane_id, is_locked=False).first()
    
    @classmethod
    def find_name_airplane(cls, name_airplane):
        return cls.query.filter_by(name_airplane=name_airplane).first()

    @classmethod
    def find_name_airplane_with_locked(cls, name_airplane):
        return cls.query.filter_by(name_airplane=name_airplane, is_locked=False).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()