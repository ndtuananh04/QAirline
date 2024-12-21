import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse
from database import db
from flask import jsonify, session, request
from core.auth import authorized_required
from models.ticketsDB import Tickets
from models.airplanesDB import Airplanes
from models.seatsDB import Seats
from services.seatS import SeatService

class SeatsAirplane(Resource):    
    parser = reqparse.RequestParser()
    parser.add_argument('seat_number', type=str, required=True, help="This field cannot be left blank!")
    def post(self):
        data = SeatsAirplane.parser.parse_args()
        seat_number = data['seat_number']
        
        ticket_id = session.get('ticket_id')
        if not ticket_id:
            return {"msg": "Chưa đăng nhập, vui lòng kiểm tra lại thông tin!"}, 400
        
        ticket = Tickets.find_ticket_id(ticket_id)
        if not ticket:
            return {"msg": "Không tìm thấy vé"}, 404
        
        print(f"Ticket ID: {ticket_id}, Seat Number: {seat_number}")
        
        exist_ticket = Tickets.find_seat_number(ticket_id, seat_number)
        if exist_ticket:
            return {"msg": "Ghế đã được chọn, vui lòng chọn ghế khác"}, 404
        
        ticket.seat_number = seat_number
        db.session.commit()
        return {"msg": "Chọn ghế thành công"}, 200
    
class SeatsAdmin(Resource):
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):
        seats = Seats.get_all_seats()
        
        if not seats:
            return {"msg": "Không tìm thấy dữ liệu"}, 404
        
        return seats
    
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        data = request.get_json()
        seat_number = data['seat_number']
        airplane_id = data['airplane_id']
        seat_class = data['seat_class']
        price = data['price']
        
        if not SeatService.validate_seat_number(seat_number):
            return {"msg": "Số ghế phải có độ dài từ 2-3 ký tự và kết thúc bằng A-F"}, 400
        
        seat = Seats(airplane_id, seat_number, seat_class, price)
        db.session.add(seat)
        db.session.commit()
        
        return {"msg": "Thêm ghế thành công"}, 200
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self, seat_id):
        seat = Seats.find_seat_id(seat_id)
        if not seat:
            return {"msg": "Không tìm thấy ghế"}, 404
        
        db.session.delete(seat)
        db.session.commit()
        return {"msg": "Xóa ghế thành công"}, 200
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def put(self, seat_id):
        data = request.get_json()
        seat_number = data['seat_number']
        airplane_id = data['airplane_id']
        seat_class = data['seat_class']
        price = data['price']
        
        seat = Seats.find_seat_id(seat_id)
        if not seat:
            return {"msg": "Không tìm thấy ghế"}, 404
        
        if not SeatService.validate_seat_number(seat_number):
            return {"msg": "Số ghế phải có độ dài từ 2-3 ký tự và kết thúc bằng A-F"}, 400
        
        if not Airplanes.find_airplane_id(airplane_id):
            return {"msg": "Không tìm thấy máy bay"}, 404
        
        seat.seat_number = seat_number
        seat.airplane_id = airplane_id
        seat.seat_class = seat_class
        seat.price = price
        db.session.commit()
        
        return {"msg": "Cập nhật ghế thành công"}, 200
    
    
        
        
        