import os
from flask import session
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse
from models.ticketsDB import Tickets, TicketUser

class CheckinC(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('ticket_number', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('phone_number', type=str, required=True, help="This field cannot be left blank!")
    
    def post(self):
        data = CheckinC.parser.parse_args()
        ticket_number = data['ticket_number']
        phone_number = data['phone_number']
        
        ticket = Tickets.find_ticket_number(ticket_number)
        if not ticket:
            return {"msg": "Không tìm thấy số vé"}, 404
    
        ticket_id = ticket.ticket_id
        phone = Tickets.find_phone_number(ticket_id, phone_number)
        if not phone:
            return {"msg": "Số điện thoại không đúng"}, 404
        
        session['ticket_id'] = ticket_id
        return {"msg": "Thông tin đúng xin mời bạn chọn ghế!"}, 200 
