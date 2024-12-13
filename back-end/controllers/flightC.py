import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from flask_restful import Resource, reqparse
from models.accountDB import Account, AccountType
from models.flightsDB import Flights, FlightDelay
from models.airplanesDB import Airplanes
from core.auth import authorized_required
from database import db
from flask import jsonify, session, request
from services.flightS import valid_date, valid_time

class DepartureArrival(Resource):
    def get(self):
        departure = Flights.query.with_entities(Flights.departure).distinct().all()
        arrival = Flights.query.with_entities(Flights.arrival).distinct().all()
        
        return jsonify({
            "departure": [d[0] for d in departure],
            "arrival": [a[0] for a in arrival]
        })
    
SEAT_ORDER = ["BUSINESS", "SKYBOSS", "ECONOMY"]
class FlightSearch(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('departure', type=str, required=True, help="Departure location is required")
    parser.add_argument('arrival', type=str, required=True, help="Arrival location is required")
    parser.add_argument('departure_time', type=str, required=True, help="Departure time is required")
    def post(self):
        data = FlightSearch.parser.parse_args()
        departure = data['departure']
        arrival = data['arrival']
        departure_time = data['departure_time']

        try:
            departure_time = datetime.strptime(departure_time, "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "Invalid departure time format"}), 400

        flights = Flights.find_flights_with_seats(departure, arrival, departure_time)

        if flights:
            for flight in flights:
                flight["seats"] = sorted(
                    flight["seats"],
                    key=lambda seat: SEAT_ORDER.index(seat["seat_class"])
                )
            session['flights'] = flights
            return flights
        else:
            return jsonify({"message": "No flights found"}), 404

class FlightAdmin(Resource):
    #Admin xem tất cả chuyến bay
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):
        flights = Flights.get_all_flights()
        return flights

    #Admin thêm chuyến bay mới
    flight_parser = reqparse.RequestParser()
    flight_parser.add_argument('flight_number', type=str, required=True, help="Flight number is required")
    flight_parser.add_argument('departure', type=str, required=True, help="Departure location is required")
    flight_parser.add_argument('code_departure', type=str, required=True, help="Code departure is required")
    flight_parser.add_argument('arrival', type=str, required=True, help="Arrival location is required")
    flight_parser.add_argument('code_arrival', type=str, required=True, help="Code arrival is required")
    flight_parser.add_argument('departure_time', type=valid_date, required=True, help="Departure time (format: YYYY-MM-DD)")
    flight_parser.add_argument('departure_hour_time', type=valid_time, required=True, help="Departure time (format: HH:MM)")
    flight_parser.add_argument('arrival_hour_time', type=valid_time, required=True, help="Arrival time (format: HH:MM)")
    flight_parser.add_argument('boarding_time', type=valid_time, required=True, help="Boarding Time is required")
    flight_parser.add_argument('terminal', type=int, required=True, help="Terminal is required")
    flight_parser.add_argument('status', type=str, required=True, help="Flight status is required")
    flight_parser.add_argument('available_seats', type=int, required=True, help="Available seats are required")
    flight_parser.add_argument('airplane_id', type=int, required=True, help="Airplane ID is required")
    

    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        data = FlightAdmin.flight_parser.parse_args()

        airplane = Airplanes.find_airplane_id(data['airplane_id'])
        if not airplane:
            return {'msg': 'Airplane not found'}, 400

        # Thêm chuyến bay vào cơ sở dữ liệu
        new_flight = Flights(
            flight_number=data['flight_number'],
            departure=data['departure'],
            code_departure=data['code_departure'],
            arrival=data['arrival'],
            code_arrival=data['code_arrival'],
            departure_time=data['departure_time'],
            departure_hour_time=data['departure_hour_time'],
            arrival_hour_time=data['arrival_hour_time'],
            boarding_time=data['boarding_time'],
            terminal=data['terminal'],
            status=data['status'],
            available_seats=data['available_seats'],
            airplane_id=data['airplane_id']
        )
        new_flight.save_to_db()
        db.session.commit()

        return {'msg': 'Flight added successfully'}, 201
    
    delete_parser = reqparse.RequestParser()
    delete_parser.add_argument('flight_id', type=int, help="Flight Id")
    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self):
        # Kiểm tra xem chuyến bay có tồn tại hay không
        data = FlightAdmin.delete_parser.parse_args()
        flight = Flights.query.filter_by(flight_id=data['flight_id']).first()

        if not flight:
            return {'msg': 'Flight not found'}, 400

        # Xóa chuyến bay khỏi cơ sở dữ liệu
        db.session.delete(flight)
        db.session.commit()

        new_flights = Flights.get_all_flights()
        return {'msg': 'Flight delete successfully', 'flights': new_flights}, 201

    
    update_parser = reqparse.RequestParser()
    update_parser.add_argument('flight_id', type=str, help="Flight Id")
    update_parser.add_argument('flight_number', type=str, help="Flight number")
    update_parser.add_argument('departure', type=str, help="Departure location")
    update_parser.add_argument('arrival', type=str, help="Arrival location")
    update_parser.add_argument('departure_time', type=str, help="Departure time (format: YYYY-MM-DD HH:MM:SS)")
    update_parser.add_argument('status', type=str, help="Flight status (SCHEDULED, DELAYED, CANCELLED)")
    update_parser.add_argument('available_seats', type=int, help="Available seats")
    update_parser.add_argument('airplane_id', type=str, help="Airplane ID")
    #Admin cập nhật thông tin chuyến bay
    @jwt_required()
    @authorized_required(roles=["admin"])
    def put(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user)

        if not account:
            return {'msg': 'Account not found'}, 400
        
        # Lấy dữ liệu từ request
        data = FlightAdmin.update_parser.parse_args()

        # Kiểm tra xem chuyến bay có tồn tại không
        flight = Flights.query.filter_by(flight_id=data['flight_id']).first()
        if not flight:
            return {'msg': 'Flight not found'}, 404

        # Cập nhật các thông tin chuyến bay nếu có
        if data['flight_number']:
            flight.flight_number = data['flight_number']
        if data['departure']:
            flight.departure = data['departure']
        if data['arrival']:
            flight.arrival = data['arrival']
        if data['departure_time']:
            flight.departure_time = data['departure_time']
        if data['status']:
            flight.status = data['status']
        if data['available_seats'] is not None:
            flight.available_seats = data['available_seats']
        if data['airplane_id']:
            # Kiểm tra xem `airplane_id` mới có tồn tại không
            airplane = Airplanes.find_airplane_id(data['airplane_id'])
            if not airplane:
                return {'msg': 'Airplane not found'}, 400
            flight.airplane_id = data['airplane_id']

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()
        return {'msg': 'Flight updated successfully'}, 201