from datetime import date
from database import db
from sqlalchemy.sql import func
from flask import jsonify

class Airplanes(db.Model):
    __tablename__ = 'airplanes'
    airplane_id = db.Column(db.Integer, primary_key=True)
    name_airplane = db.Column(db.String(10), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_locked = db.Column(db.Integer, default=0)

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
    
    @classmethod
    def get_all_airplanes(cls):
        airplanes = db.session.query(
            Airplanes.airplane_id,
            Airplanes.name_airplane,
            Airplanes.capacity,
            Airplanes.is_locked
        ).all()

        airplanes_list = {}

        for airplane in airplanes:
            if airplane.airplane_id not in airplanes_list:
                airplanes_list[airplane.airplane_id] = {
                    "airplane_id": airplane.airplane_id,
                    "name_airplane": airplane.name_airplane,
                    "capacity": airplane.capacity,
                    "is_locked": airplane.is_locked
                }
            results = list(airplanes_list.values())
        return results
    
    @classmethod
    def find_airplane_id(cls, airplane_id):
        return cls.query.filter_by(airplane_id=airplane_id).first()
    
    @classmethod
    def find_name_airplane(cls, name_airplane):
        return cls.query.filter_by(name_airplane=name_airplane).first()

    @classmethod
    def find_name_airplane_with_locked(cls, airplane_id):
        return cls.query.filter_by(airplane_id=airplane_id, is_locked=0).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()