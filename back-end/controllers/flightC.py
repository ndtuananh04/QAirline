import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from flask_restful import Resource, reqparse
from models.accountDB import Account, AccountType
from models.flightsDB import Flights, FlightDelay
from models.airplanesDB import Airplanes
from services.flightS import FlightService, valid_date, valid_time
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
    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        data = request.get_json()
        flight_number = data['flight_number']
        airplane_id = data['airplane_id']
        departure_time = datetime.strptime(data['departure_time'], '%Y-%m-%d')
        departure_hour_time = datetime.strptime(data['departure_hour_time'], '%H:%M')
        arrival_hour_time = datetime.strptime(data['arrival_hour_time'], '%H:%M')
        boarding_time = datetime.strptime(data['boarding_time'], '%H:%M')
        departure = data['departure']
        arrival = data['arrival']
        code_departure = data['code_departure']
        code_arrival = data['code_arrival'] 
        
        
        if not FlightService.check_flight_number(flight_number):
            return {'msg': 'Số chuyến bay phải gồm 6 chữ số và QAL.'}, 400
        
        if not FlightService.check_location(departure):
            return {'msg': 'Địa điểm không hợp lệ.'}, 400
        
        if not FlightService.check_location(arrival):
            return {'msg': 'Địa điểm không hợp lệ.'}, 400
        
        if not FlightService.check_code(code_departure):
            return {'msg': 'Mã không hợp lệ.'}, 400
        
        if not FlightService.check_code(code_arrival):
            return {'msg': 'Mã không hợp lệ.'}, 400
        
        # Kiểm tra xem chuyến bay đã tồn tại hay chưa
        flight = Flights.find_flight_number(flight_number)
        if flight:
            return {'msg': 'Chuyến bay đã tồn tại.'}, 400
        
        airplane = Airplanes.find_airplane_id(airplane_id)
        if not airplane:
            return {'msg': 'Không tìm thấy máy bay'}, 400

        # Thêm chuyến bay vào cơ sở dữ liệu
        new_flight = Flights(
            flight_number=flight_number,
            departure=departure,
            code_departure=code_departure,
            arrival=arrival,
            code_arrival=code_arrival,
            departure_time=departure_time,
            departure_hour_time=departure_hour_time,
            arrival_hour_time=arrival_hour_time,
            boarding_time=boarding_time,
            terminal=data['terminal'],
            status=data['status'],
            airplane_id=data['airplane_id'],
            is_locked=False
        )
        new_flight.save_to_db()

        return {'msg': 'Thêm chuyến bay thành công.'}, 201

    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self, flight_id):
        # Kiểm tra xem chuyến bay có tồn tại hay không
        flight = Flights.find_flight_id(flight_id)

        if not flight:
            return {'msg': 'Không tìm thấy chuyến bay.'}, 400

        flight.is_locked = 0 if flight.is_locked == 1 else 1

        db.session.commit()

        if flight.is_locked == 1:
            return {'msg': 'Khóa chuyến bay thành công.'}, 201
        else:
            return {'msg': 'Mở khóa chuyến bay thành công.'}, 200
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def put(self, flight_id):
        data = request.get_json()
        
        # Kiểm tra xem chuyến bay có tồn tại không
        flight = Flights.find_flight_id(flight_id)
        if not flight:
            return {'msg': 'Chuyến bay không tồn tại'}, 400
        
        # Cập nhật các thông tin chuyến bay nếu có
        if data['flight_number']:
            flight.flight_number = data['flight_number']
        if data['departure']:
            flight.departure = data['departure']
        if data['code_departure']:
            flight.code_departure = data['code_departure']
        if data['arrival']:
            flight.arrival = data['arrival']
        if data['code_arrival']:
            flight.code_arrival = data['code_arrival']
        if data['departure_time']:
            flight.departure_time = data['departure_time']
        if data['departure_hour_time']:
            flight.departure_hour_time = data['departure_hour_time']
        if data['arrival_hour_time']:
            flight.arrival_hour_time = data['arrival_hour_time']
        if data['boarding_time']:
            flight.boarding_time = data['boarding_time']
        if data['status']:
            flight.status = data['status']
        if data['airplane_id']:
            airplane = Airplanes.find_airplane_id(data['airplane_id'])
            if not airplane:
                return {'msg': 'Không tìm thấy máy bay.'}, 400
            flight.airplane_id = data['airplane_id']

        db.session.commit()
        return {'msg': 'Cập nhật chuyến bay thành công.'}, 200