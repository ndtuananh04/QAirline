from datetime import date
from database import db
from sqlalchemy.sql import func
import enum
from models.airplaneDB import Airplane
from models.seatsDB import Seats

class FlightType(enum.Enum):
    SCHEDULED = 1
    DELAYED = 2
    CANCELLED = 3

class Flight(db.Model):
    __tablename__ = 'flight'
    flight_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_number = db.Column(db.String(45), unique=True, nullable=False)
    departure = db.Column(db.String(60), nullable=False)
    arrival = db.Column(db.String(60), nullable=False)
    departure_time = db.Column(db.DateTime(timezone=True), nullable=False)
    arrival_time = db.Column(db.DateTime(timezone=True), nullable=False)
    status = db.Column(db.Enum(FlightType), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    airplane_id = db.Column(db.String(60), db.ForeignKey('airplane.airplane_id'), onupdate="CASCADE")

    def __init__(self, flight_id, flight_number, departure, arrival, departure_time, arrival_time, status, available_seats):
        self.flight_id = flight_id
        self.flight_number = flight_number
        self.departure = departure
        self.arrival = arrival
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.status = status
        self.available_seats = available_seats

    def to_json(self):
        return {
            "flight_id": self.flight_id,
            "flight_number" : self.flight_number,
            "departure": self.departure,
            "arrival": self.arrival,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "status": self.status,
            "available_seats": self.available_seats
        }

    @classmethod
    def find_flights(cls, departure, arrival, departure_time):
        return cls.query.filter_by(
            departure=departure,
            arrival=arrival,
            departure_time=departure_time
        ).all()

    '''
    Tìm chuyến bay dựa trên điểm khởi hành, điểm đến và thời gian khởi hành
    Trả về thông tin về tất cả chuyến bay, hạng ghế và giá
    '''
    @classmethod
    def find_flights_with_seats(cls, departure, arrival, departure_time):
    # Sử dụng JOIN để kết nối các bảng Flight, Airplane và Seats
        flights = db.session.query(
            Flight.flight_id,
            Flight.flight_number,
            Flight.departure,
            Flight.arrival,
            Flight.departure_time,
            Flight.arrival_time,
            Flight.status,
            Flight.available_seats,
            Seats.seat_class,
            Seats.price
        ).select_from(Flight). \
            join(Airplane, Flight.airplane_id == Airplane.airplane_id). \
            join(Seats, Airplane.airplane_id == Seats.airplane_id). \
            filter(Flight.departure == departure). \
            filter(Flight.arrival == arrival). \
            filter(Flight.departure_time == departure_time). \
            all()

        # Chuyển đổi kết quả thành định dạng JSON hợp lệ
        results = []
        for flight in flights:
            flight_data = {
                "flight_id": flight.flight_id,
                "flight_number": flight.flight_number,
                "departure": flight.departure,
                "arrival": flight.arrival,
                "departure_time": flight.departure_time,
                "arrival_time": flight.arrival_time,
                "status": flight.status.name,
                "available_seats": flight.available_seats,
                "seats": []
            }

            flight_data["seats"].append({
                "seat_class": flight.seat_class.name,
                "price": str(flight.price)  # Chuyển Decimal thành string
            })

            results.append(flight_data)

        return results
    
    @classmethod
    def find_flight_id(cls, flight_id):
        return cls.query.filter_by(flight_id=flight_id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
class FlightDelay(db.Model):
    __tablename__ = 'flight_delay'
    delay_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.flight_id'), nullable=False)
    new_departure_time = db.Column(db.DateTime())

    def __init__(self, delay_id, new_departure_time):
        self.delay_id = delay_id   
        self.new_departure_time = new_departure_time

    def to_json(self):
        return {
            "delay_id": self.delay_id,
            "new_departure_time": self.new_departure_time,
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()