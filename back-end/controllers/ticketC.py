import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from flask_restful import Resource, reqparse
from models.accountDB import Account, AccountType
from models.flightsDB import Flights, FlightDelay
from models.airplanesDB import Airplanes
from models.seatsDB import Seats
from models.ticketsDB import Tickets, TicketUser, StatusClass
from core.auth import authorized_required

from services.ticketS import TicketS
from database import db
from flask import jsonify, session, request
    
class SelectTicket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('flight_id', type=int, required=True, help="Flight ID is required")
    parser.add_argument('seat_class', type=str, required=True, help="Seat class is required")
    parser.add_argument('price', type=float, required=True, help="Price is required")
    parser.add_argument('quantity', type=int, required=True, help="Quantity is required")

    def post(self):
        data = self.parser.parse_args()
        flight_id = data['flight_id']
        seat_class = data['seat_class']
        price = data['price']
        quantity = data['quantity']

        # Kiểm tra thông tin chuyến bay trong session
        flights = session.get('flights', [])
        if not flights:
            return {"message": "No flight data in session"}, 400
        
        # Tìm kiếm chuyến bay và loại ghế
        selected_flight = next((flight for flight in flights if flight['flight_id'] == flight_id), None)
        if not selected_flight:
            return {"message": f"Flight ID {flight_id} not found"}, 404
        
        selected_seat = next(
            (seat for seat in selected_flight.get("seats", []) if seat["seat_class"].upper() == seat_class.upper()),
            None
        )
        if not selected_seat:
            return {"message": f"Seat class '{seat_class}' not found in flight {flight_id}"}, 404
        
        total_price = price * quantity
        vat = total_price * 0.1
        grand_total = total_price + vat

        # Lưu thông tin vào session
        session['selected_ticket'] = {
            'flight_id': flight_id,
            'seat_class': seat_class,
            'price': price,
            'quantity': quantity,
            'total_price': total_price,
            'vat': vat,
            'grand_total': grand_total
        }

        return {
            "message": "Seat selected successfully",
            "details": {
                "total_price": total_price,
                "vat": vat,
                "grand_total": grand_total
            }
        }, 200
                
# Customer xem vé, điền thông tin vé, hủy vé
class TicketCustomer(Resource):
    @jwt_required()
    @authorized_required(roles=["customer"])
    def get(self):
        account_id = get_jwt_identity()
        tickets = Tickets.get_all_ticket_account_id(account_id)
        
        if tickets:
            return jsonify(tickets)
        else:
            return {"message": "No tickets found"}, 400
        
    parser = reqparse.RequestParser()
    parser.add_argument('identification', type=str, required=True, help="Indentification number is required")
    parser.add_argument('family_name', type=str, required=True, help="Family name is required")
    parser.add_argument('given_name', type=str, required=True, help="Given name is required")
    parser.add_argument('gender', type=str, required=True, help="Gender is required")
    parser.add_argument('nationality', type=str, required=True, help="Nationality is required")
    parser.add_argument('phone_number', type=str, required=True, help="Phone number is required")
    parser.add_argument('email', type=str, required=True, help="Email is required")
    
    @jwt_required()
    @authorized_required(roles=["customer"])
    def post(self):
        account_id = get_jwt_identity()
        data = self.parser.parse_args()

        # Kiểm tra và lấy flight_id và seat_class từ session
        selected_ticket = session.get('selected_ticket')
        if not selected_ticket:
            return {"message": "No selected ticket information found in session"}, 400

        flight_id = selected_ticket.get('flight_id')
        seat_class = selected_ticket.get('seat_class')

        if not flight_id or not seat_class:
            return {"message": "Incomplete flight information in session"}, 400
        
        new_ticket = Tickets(
            account_id=account_id,
            flight_id=flight_id,
            ticket_number=TicketS.generate_custom_random_string(),
            seat_number=None,
            seat_class=seat_class,
            booking_time=datetime.now(),
            status="scheduled"
        )
        db.session.add(new_ticket)
        db.session.commit()

        new_ticket_user = TicketUser(
            ticket_id=new_ticket.ticket_id,
            identification=data['identification'],
            family_name=data['family_name'],
            given_name=data['given_name'],
            gender=data['gender'],
            nationality=data['nationality'],
            phone_number=data['phone_number'],
            email=data['email']
        )
        db.session.add(new_ticket_user)
        db.session.commit()

        return {"msg": "Ticket created successfully"}, 200

    @jwt_required()
    @authorized_required(roles=["customer"])
    def put(self, ticket_id):
        account_id = get_jwt_identity()
        ticket = Tickets.find_ticket_id(ticket_id)
        
        if not ticket:
            return {'msg': 'Ticket not found'}, 400
        
        if ticket.account_id != account_id:
            return {'msg': 'Unauthorized'}, 401
        
        ticket.status = StatusClass.cancelled
        db.session.commit()
        return {'msg': 'Ticket cancelled successfully'}, 200

class TicketAdmin(Resource):
    parser = reqparse.RequestParser()
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])
        
        if not account:
            return {'msg': 'Account not found'}, 400
        
        flights = Flights.query.all()
        if flights:
            return jsonify({"flights": flights}), 200
        else:
            return jsonify({"message": "No flights found"}), 400
        
    @jwt_required()
    @authorized_required(roles=["customer"])
    def post(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])
        
        if not account:
            return {'msg': 'Account not found'}, 400

        data = TicketAdmin.parser.parse_args()
        
        flight_id = data['flight_number']
        if not Flights.find_flight_id(flight_id):
            return {'msg': 'Flight not found'}, 400
        
        new_ticket = Tickets(
            ticket_number=TicketS.generate_custom_random_string(),
            flight_id=data['flight_id'],
            ticket_class=data['ticket_class']
        )
        db.session.add(new_ticket)
        db.session.commit()
        
        return {'msg': 'Ticket added successfully'}, 200

    parser_delete = reqparse.RequestParser()
    parser_delete.add_argument('ticket_id', type=str, required=True, help="Ticket ID is required")
    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])
        
        if not account:
            return {'msg': 'Account not found'}, 400
        
        data = TicketAdmin.parser_delete.parse_args()
        
        ticket_id = data['ticket_id']
        ticket = Tickets.find_ticket_id(ticket_id)

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
    @authorized_required(roles=["admin"])
    def put(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])
        
        if not account:
            return {'msg': 'Account not found'}, 400
        
        data = TicketAdmin.parser_update.parse_args()
        
        ticket_id = data['ticket_id']
        ticket = Tickets.find_ticket_id(ticket_id)
        
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
