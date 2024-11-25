from datetime import datetime
from database import db
from sqlalchemy.sql import func
import enum
from models.airplanesDB import Airplanes
from models.seatsDB import Seats
from flask import jsonify

class FlightType(enum.Enum):
    SCHEDULED = "scheduled"
    DELAYED = "delayed"
    CANCELLED = "cancelled"

    @classmethod
    def from_string(cls, value):
        try:
            return cls[value.upper()]  # Chuyển giá trị thành chữ hoa trước khi đối chiếu
        except KeyError:
            raise ValueError(f"Invalid flight type: {value}")

class Flights(db.Model):
    __tablename__ = 'flights'
    flight_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_number = db.Column(db.String(45), unique=True, nullable=False)
    departure = db.Column(db.String(60), nullable=False)
    arrival = db.Column(db.String(60), nullable=False)
    departure_time = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(FlightType), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    airplane_id = db.Column(db.Integer, db.ForeignKey('airplanes.airplane_id'), onupdate="CASCADE")

    def __init__(self, flight_number, departure, arrival, departure_time, status, available_seats):
        self.flight_number = flight_number
        self.departure = departure
        self.arrival = arrival
        self.departure_time = departure_time
        self.status = FlightType.from_string(status.upper())
        self.available_seats = available_seats

    def to_json(self):
        return {
            "flight_number" : self.flight_number,
            "departure": self.departure,
            "arrival": self.arrival,
            "departure_time": self.departure_time.strftime('%Y-%m-%d'),
            "status": self.status.name,
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
        flights = db.session.query(
            Flights.flight_number,
            Flights.departure,
            Flights.arrival,
            Flights.departure_time,
            Seats.seat_class,
            Seats.price
        ).select_from(Flights). \
            join(Airplanes, Flights.airplane_id == Airplanes.airplane_id). \
            join(Seats, Airplanes.airplane_id == Seats.airplane_id). \
            filter(Flights.departure == departure). \
            filter(Flights.arrival == arrival). \
            filter(Flights.departure_time == departure_time). \
            all()

        flight_dict = {}

        for flight in flights:
            if flight.flight_number not in flight_dict:
                flight_dict[flight.flight_number] = {
                    "flight_number": flight.flight_number,
                    "departure": flight.departure,
                    "arrival": flight.arrival,
                    "departure_time": flight.departure_time.strftime('%Y-%m-%d'),
                    "seats": []
                }

            seat = {
                "seat_class": flight.seat_class.name if isinstance(flight.seat_class, enum.Enum) else str(flight.seat_class),
                "price": float(flight.price)
            }

            # Kiểm tra xem hạng ghế này đã có trong seats chưa
            if seat not in flight_dict[flight.flight_number]["seats"]:
                flight_dict[flight.flight_number]["seats"].append(seat)
            results = list(flight_dict.values())

        return jsonify(results)
    
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