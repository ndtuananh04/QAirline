import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from models.accountDB import Account, AccountType
from models.seatsDB import Seats
from core.auth import authorized_required
from database import db
from flask import jsonify, session, request
from models.ticketsDB import Tickets

class SeatsAirplane(Resource):
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):
        seats = Seats.get_all_seats()
        return seats
    
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
        
        
        