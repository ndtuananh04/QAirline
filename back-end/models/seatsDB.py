import enum
from database import db
from sqlalchemy.sql import func
from flask import jsonify
from models.airplanesDB import Airplanes


class SeatClass(enum.Enum):
    ECONOMY = "ECONOMY"
    SKYBOSS = "SKYBOSS"
    BUSINESS = "BUSINESS"

    @classmethod
    def from_string(cls, value):
        try:
            return cls[value.upper()]  # Chuyển giá trị thành chữ hoa trước khi đối chiếu
        except KeyError:
            raise ValueError(f"Invalid flight type: {value}")

class Seats(db.Model):
    __tablename__ = 'seats'
    seat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    airplane_id = db.Column(db.Integer, db.ForeignKey('airplanes.airplane_id'))
    seat_number = db.Column(db.String(10), nullable=False)
    seat_class = db.Column(db.Enum(SeatClass), nullable=False)
    price = db.Column(db.Numeric(10, 0), nullable=False)

    def __init__(self, airplane_id, seat_number, seat_class, price):
        self.airplane_id = airplane_id
        self.seat_number = seat_number
        self.seat_class = SeatClass.from_string(seat_class.upper())
        self.price = price

    def to_json(self):
        return {
            "airplane_id": self.airplane_id,
            "seat_number": self.seat_number,
            "seat_class": self.seat_class.name,
            "price": self.price
        }
    
    @classmethod
    def find_seat_id(cls, seat_id):
        return cls.query.filter_by(seat_id=seat_id).first()
    
    @classmethod
    def find_airplane_id(cls, airplane_id):
        return cls.query.filter_by(airplane_id=airplane_id).first()
    
    @classmethod
    def get_all_seats(cls):
        # Lấy dữ liệu từ database và sắp xếp
        seats = db.session.query(
            Seats.seat_id,
            Seats.airplane_id,
            Seats.seat_number,
            Seats.seat_class,
            Seats.price
        ).order_by(
            Seats.airplane_id.asc(),  # Sắp xếp airplane_id tăng dần
            Seats.price.asc()        # Sắp xếp price giảm dần
        ).all()
        
        # Xử lý dữ liệu và định dạng kết quả
        seats_list = []
        
        for seat in seats:
            seats_list.append({
                "seat_id": seat.seat_id,
                "airplane_id": seat.airplane_id,
                "seat_number": seat.seat_number,
                "seat_class": str(seat.seat_class.name),
                "price": "{:,.0f}".format(float(seat.price)).replace(",", ".")  # Định dạng giá tiền
            })
        
        return seats_list
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()