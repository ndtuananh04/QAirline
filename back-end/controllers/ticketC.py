import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from flask_restful import Resource, reqparse
from models.accountDB import Account, AccountType
from models.flightDB import Flight, FlightDelay
from models.airplaneDB import Airplane
from models.seatsDB import Seats
from models.ticketDB import Ticket

from services.ticketS import TicketS
#from services.flightS import FlightS
from database import db
from flask import jsonify

class TicketSearch(Resource):
    parser = reqparse.RequestParser()
    @jwt_required()
    def get(sekf):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])
        
        if not account:
            return {'msg': 'Account not found'}, 400
        
        if account.role != AccountType.ADMIN:
            return {'msg': 'Access forbidden: Only admins can view flights'}, 400
        
        flights = Flight.query.all()
        if flights:
            return jsonify({"flights": flights}), 200
        else:
            return jsonify({"message": "No flights found"}), 400
        
    @jwt_required()
    def post(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])
        
        if not account:
            return {'msg': 'Account not found'}, 400
        
        if account.role != AccountType.CUSTOMER:
            return {'msg': 'Access forbidden: Only customer can add flights'}, 400
        
        data = TicketSearch.parser.parse_args()
        
        flight_id = data['flight_number']
        if not Flight.find_flight_id(flight_id):
            return {'msg': 'Flight not found'}, 400
        
        new_ticket = Ticket(
            ticket_number=TicketS.generate_ticket_number(),
            flight_id=data['flight_id'],
            ticket_class=data['ticket_class']
        )
        
        return {'msg': 'Flight added successfully'}, 200

    parser_delete = reqparse.RequestParser()
    parser_delete.add_argument('ticket_id', type=str, required=True, help="Ticket ID is required")
    @jwt_required()
    def delete(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])
        
        if not account:
            return {'msg': 'Account not found'}, 400
        
        if account.role != AccountType.ADMIN:
            return {'msg': 'Access forbidden: Only admins can delete flights'}, 400
        
        data = TicketSearch.parser_delete.parse_args()
        
        ticket_id = data['ticket_id']
        ticket = Ticket.find_ticket_id(ticket_id)

        if not ticket:
            return {'msg': 'Flight not found'}, 400
        
        db.session.delete(ticket)
        db.session.commit()
        return {'msg': 'Flight deleted successfully'}, 200
    
    parser_update = reqparse.RequestParser()
    parser_update.add_argument('ticket_id', type=str, required=True, help="Ticket ID is required")
    parser_update.add_argument('ticket_number', type=str, help="Ticket number")
    parser_update.add_argument('flight_id', type=str, help="Flight ID")
    parser_update.add_argument('ticket_class', type=str, help="Ticket class")

    @jwt_required()
    def put(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])
        
        if not account:
            return {'msg': 'Account not found'}, 400
        
        if account.role != AccountType.ADMIN:
            return {'msg': 'Access forbidden: Only admins can update flights'}, 400
        
        data = TicketSearch.parser_update.parse_args()
        
        ticket_id = data['ticket_id']
        ticket = Ticket.find_ticket_id(ticket_id)
        
        if not ticket:
            return {'msg': 'Flight not found'}, 400
        
        if data['ticket_number']:
            ticket.ticket_number = data['ticket_number']
        if data['flight_id']:
            ticket.flight_id = data['flight_id']
        if data['ticket_class']:
            ticket.ticket_class = data['ticket_class']
        
        db.session.commit()
        return {'msg': 'Flight updated successfully'}, 200
