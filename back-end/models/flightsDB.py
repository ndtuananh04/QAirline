from datetime import datetime, time
from database import db
from sqlalchemy.sql import func
import enum
from models.airplanesDB import Airplanes
from models.seatsDB import Seats
from flask import jsonify
from collections import OrderedDict

class FlightType(enum.Enum):
    SCHEDULED = "scheduled"
    DELAYED = "delayed"
    CANCELLED = "cancelled"
    FINISHED = "finished"

    @classmethod
    def from_string(cls, value):
        try:
            return cls[value.upper()]  # Chuyển giá trị thành chữ hoa trước khi đối chiếu
        except KeyError:
            raise ValueError(f"Invalid flight type: {value}")

class Flights(db.Model):
    __tablename__ = 'flights'
    flight_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_number = db.Column(db.String(10), unique=True, nullable=False)
    departure = db.Column(db.String(60), nullable=False)
    code_departure = db.Column(db.String(60), nullable=False)
    arrival = db.Column(db.String(10), nullable=False)
    code_arrival = db.Column(db.String(10), nullable=False)
    departure_time = db.Column(db.Date, nullable=False)
    departure_hour_time = db.Column(db.Time, nullable=False)
    arrival_hour_time = db.Column(db.Time, nullable=False)
    boarding_time = db.Column(db.Time, nullable=False)
    terminal = db.Column(db.Integer , nullable=False)
    status = db.Column(db.Enum(FlightType), nullable=False)
    airplane_id = db.Column(db.Integer, db.ForeignKey('airplanes.airplane_id'))
    is_locked = db.Column(db.Integer, default=0)

    def __init__(self, flight_number, departure, code_departure, arrival, code_arrival, departure_time, departure_hour_time, arrival_hour_time, boarding_time, terminal, status, airplane_id, is_locked):
        self.flight_number = flight_number
        self.departure = departure
        self.code_departure = code_departure
        self.arrival = arrival
        self.code_arrival = code_arrival
        self.departure_time = departure_time
        self.departure_hour_time = departure_hour_time.strftime('%H:%M') if departure_hour_time else None
        self.arrival_hour_time = arrival_hour_time.strftime('%H:%M') if arrival_hour_time else None
        self.boarding_time = boarding_time.strftime('%H:%M') if boarding_time else None
        self.terminal = terminal
        self.status = FlightType.from_string(status.upper())
        self.airplane_id = airplane_id,
        self.is_locked = self.is_locked

    def to_json(self):
        return {
            "flight_number" : self.flight_number,
            "departure": self.departure,
            "code_departure": self.code_departure,
            "arrival": self.arrival,
            "code_arrival": self.code_arrival,
            "departure_time": self.departure_time.strftime('%Y-%m-%d'),
            "departure_hour_time": self.departure_hour_time.strftime('%H:%M'),
            "arrival_hour_time": self.arrival_hour_time.strftime('%H:%M'),
            "boarding_time": self.boarding_time.strftime('%H:%M'),
            "terminal": self.terminal,
            "status": self.status.name,
            "airplane_id": self.airplane_id,
            "is_locked": self.is_locked
        }

    @classmethod
    def find_flights(cls, departure, arrival, departure_time):
        return cls.query.filter_by(
            departure=departure,
            arrival=arrival,
            departure_time=departure_time
        ).all()
    
    '''
    Trả về tất cả chuyến bay hiển thị ở admin
    '''
    @classmethod
    def get_all_flights(cls):
    # Truy vấn tất cả các chuyến bay với các trường cần thiết
        flights = db.session.query(
            Flights.flight_id,
            Flights.flight_number,
            Flights.departure,
            Flights.arrival,
            Flights.departure_time,
            Flights.departure_hour_time,
            Flights.status,
            Flights.airplane_id,
            Flights.is_locked
        ).all()
        flights_list = {}
        for flight in flights:
            if flight.flight_id not in flights_list:
                flights_list[flight.flight_id] = {
                    "flight_id": flight.flight_id,
                    "flight_number": flight.flight_number,
                    "departure": flight.departure,
                    "arrival": flight.arrival,
                    "departure_time": flight.departure_time.strftime('%Y-%m-%d'),
                    "departure_hour_time": flight.departure_hour_time.strftime('%H:%M'),
                    "status": flight.status.name,
                    "airplane_id": flight.airplane_id,
                    "is_locked": flight.is_locked
                }
            results = list(flights_list.values())
        return results

    '''
    Tìm chuyến bay dựa trên điểm khởi hành, điểm đến và thời gian khởi hành
    Trả về thông tin về tất cả chuyến bay, hạng ghế và giá
    '''
    @classmethod
    def find_flights_with_seats(cls, departure, arrival, departure_time):
        flights = db.session.query(
            Flights.flight_id,
            Flights.flight_number,
            Flights.departure,
            Flights.code_departure,
            Flights.arrival,
            Flights.code_arrival,
            Flights.departure_time,
            Flights.departure_hour_time,
            Flights.arrival_hour_time,
            Flights.terminal,
            Airplanes.name_airplane,
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
            if flight.flight_id not in flight_dict:
                flight_dict[flight.flight_id] = {
                    "flight_id": flight.flight_id,
                    "flight_number": flight.flight_number,
                    "departure": flight.departure,
                    "code_departure": flight.code_departure,
                    "arrival": flight.arrival,
                    "code_arrival": flight.code_arrival,
                    "departure_time": flight.departure_time.strftime('%Y-%m-%d'),
                    "departure_hour_time": flight.departure_hour_time.strftime('%H:%M'),
                    "arrival_hour_time": flight.arrival_hour_time.strftime('%H:%M'),
                    "name_airplane": flight.name_airplane,
                    "terminal": flight.terminal,
                    "seats": []
                }

            seat = {
                "seat_class": flight.seat_class.name if isinstance(flight.seat_class, enum.Enum) else str(flight.seat_class),
                "price": float(flight.price)
            }

            # Kiểm tra xem hạng ghế này đã có trong seats chưa
            if seat not in flight_dict[flight.flight_id]["seats"]:
                flight_dict[flight.flight_id]["seats"].append(seat)

        # Chuyển đổi flight_dict thành danh sách các kết quả
        results = list(flight_dict.values())

        # Trả về danh sách thay vì dùng jsonify
        return results

    
    @classmethod
    def find_flight_id(cls, flight_id):
        return cls.query.filter_by(flight_id=flight_id).first()
    
    @classmethod
    def find_flight_number(cls, flight_number):
        return cls.query.filter_by(flight_number=flight_number).first()
    
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