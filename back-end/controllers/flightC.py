import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from flask_restful import Resource, reqparse
from models.accountDB import Account, AccountType
from models.flightsDB import Flights, FlightDelay
from models.airplanesDB import Airplanes
from database import db
from flask import jsonify

class DepartureArrival(Resource):
    def get(self):
        departure = Flights.query.with_entities(Flights.departure).distinct().all()
        arrival = Flights.query.with_entities(Flights.arrival).distinct().all()
        
        return jsonify({
            "departure": [d[0] for d in departure],
            "arrival": [a[0] for a in arrival]
        })

class FlightSearch(Resource):
    #Tìm kiếm chuyến bay dựa trên các tham số
    parser = reqparse.RequestParser()
    parser.add_argument('departure', type=str, required=True, help="Departure location is required")
    parser.add_argument('arrival', type=str, required=True, help="Arrival location is required")
    parser.add_argument('departure_time', type=str, required=True, help="Departure time is required")

    def get(self):
        data = FlightSearch.parser.parse_args()
        departure = data['departure']
        arrival = data['arrival']
        departure_time = data['departure_time']

        try:
            departure_time = datetime.strptime(departure_time, "%Y-%m-%d")
        except ValueError:
            return jsonify({"message": "Invalid departure time format"}), 400

        # Tìm kiếm chuyến bay dựa trên các tham số
        flights = Flights.find_flights_with_seats(departure, arrival, departure_time)

        if flights:
            return {"flights": flights}
        else:
            return jsonify({"message": "No flights found"}), 404

    #Admin thêm chuyến bay mới
    flight_parser = reqparse.RequestParser()
    flight_parser.add_argument('flight_number', type=str, required=True, help="Flight number is required")
    flight_parser.add_argument('departure', type=str, required=True, help="Departure location is required")
    flight_parser.add_argument('arrival', type=str, required=True, help="Arrival location is required")
    flight_parser.add_argument('departure_time', type=str, required=True, help="Departure time (format: YYYY-MM-DD)")
    flight_parser.add_argument('status', type=str, required=True, help="Flight status is required")
    flight_parser.add_argument('available_seats', type=int, required=True, help="Available seats are required")
    flight_parser.add_argument('airplane_id', type=str, required=True, help="Airplane ID is required")

    @jwt_required()
    def post(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])

        if not account:
            return {'msg': 'Account not found'}, 400
        
        if account.role != AccountType.ADMIN:
            return {'msg': 'Access forbidden: Only admins can add flights'}, 400
        
        data = FlightSearch.flight_parser.parse_args()

        airplane = Airplanes.find_airplane_id(data['airplane_id'])
        if not airplane:
            return {'msg': 'Airplane not found'}, 400

        # Thêm chuyến bay vào cơ sở dữ liệu
        new_flight = Flights(
            flight_number=data['flight_number'],
            departure=data['departure'],
            arrival=data['arrival'],
            departure_time=data['departure_time'],
            status=data['status'],
            available_seats=data['available_seats'],
            airplane_id=data['airplane_id']
        )
        new_flight.save_to_db()

        return jsonify({"msg": "Flight added successfully", "flight": new_flight.to_json()}), 200

    #Admin xóa chuyến bay
    parser_delete = reqparse.RequestParser()
    parser_delete.add_argument('flight_id', type=int, required=True, help="Flight ID is required")

    @jwt_required()
    def delete(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])

        if not account:
            return {'msg': 'Account not found'}, 400
        
        if account.role != AccountType.ADMIN:
            return {'msg': 'Access forbidden: Only admins can delete flights'}, 400

        # Lấy flight_id từ request
        data = FlightSearch.parser.parse_args()
        flight_id = data['flight_id']

        # Kiểm tra xem chuyến bay có tồn tại hay không
        flight = Flights.query.filter_by(flight_id=flight_id).first()

        if not flight:
            return {'msg': 'Flight not found'}, 400

        # Xóa chuyến bay khỏi cơ sở dữ liệu
        db.session.delete(flight)
        db.session.commit()

        return jsonify({"msg": "Flight deleted successfully"}), 200

    #Admin cập nhật thông tin chuyến bay
    update_parser = reqparse.RequestParser()
    update_parser.add_argument('flight_id', type=int, required=True, help="Flight ID is required")
    update_parser.add_argument('flight_number', type=str, help="Flight number")
    update_parser.add_argument('departure', type=str, help="Departure location")
    update_parser.add_argument('arrival', type=str, help="Arrival location")
    update_parser.add_argument('departure_time', type=str, help="Departure time (format: YYYY-MM-DD HH:MM:SS)")
    update_parser.add_argument('status', type=str, help="Flight status (SCHEDULED, DELAYED, CANCELLED)")
    update_parser.add_argument('available_seats', type=int, help="Available seats")
    update_parser.add_argument('airplane_id', type=str, help="Airplane ID")

    @jwt_required()
    def put(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])

        if not account:
            return {'msg': 'Account not found'}, 400
        
        if account.role != AccountType.ADMIN:
            return {'msg': 'Access forbidden: Only admins can update flights'}, 400

        # Lấy dữ liệu từ request
        data = FlightSearch.update_parser.parse_args()

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

        return jsonify({"msg": "Flight updated successfully", "flight": flight.to_json()}), 200