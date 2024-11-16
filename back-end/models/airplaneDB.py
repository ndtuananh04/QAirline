from datetime import date
from database import db
from sqlalchemy.sql import func

class Airplane(db.Model):
    __tablename__ = 'airplane'
    airplane_id = db.Column(db.String(60), primary_key=True, autoincrement=True)
    name_airplane = db.Column(db.String(45), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def __init__(self, airplane_id, name_airplane, capacity, is_deleted):
        self.airplane_id = airplane_id
        self.name_airplane = name_airplane
        self.capacity = capacity
        self.is_deleted = is_deleted

    def to_json(self):
        return {
            "name_airplane": self.name_airplane,
            "capacity": self.capacity,
            "is_deleted": self.is_deleted
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