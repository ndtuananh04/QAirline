import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from database import db
from flask import jsonify, session, request
from models.accountDB import Account, AccountType
from models.flightsDB import Flights, FlightDelay
from models.ticketsDB import Tickets, TicketUser, StatusClass, Cancellations
from core.auth import authorized_required
from services.ticketS import TicketS

class QuantityTicket(Resource):
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):
        # Lấy danh sách vé từ hàm get_ticket_admin_dashboard
        tickets = Tickets.get_ticket_admin_dashboard()

        # Dictionary để lưu kết quả thống kê
        monthly_summary = {}
        
        for ticket in tickets:
            departure_month = ticket['departure_time'].month  # Lấy tháng từ thời gian khởi hành
            departure_year = ticket['departure_time'].year  # Lấy năm từ thời gian khởi hành
            
            seat_class = str(ticket['seat_class']).strip().lower()  # Loại ghế (business, skyboss, economy)
            
            if departure_year not in monthly_summary:
                monthly_summary[departure_year] = {}

            if departure_month not in monthly_summary[departure_year]:
                monthly_summary[departure_year][departure_month] = {
                    "business": 0,
                    "skyboss": 0,
                    "economy": 0
                }

            # Cập nhật số lượng cho từng loại ghế
            if seat_class == 'business':
                monthly_summary[departure_year][departure_month]["business"] += 1
            elif seat_class == 'skyboss':
                monthly_summary[departure_year][departure_month]["skyboss"] += 1
            elif seat_class == 'economy':
                monthly_summary[departure_year][departure_month]["economy"] += 1

        # Chuyển đổi kết quả sang danh sách để trả về
        response = []
        for year, months in monthly_summary.items():
            for month, data in sorted(months.items()):
                response.append({"year": year, "month": month, **data})

        return jsonify({"status": "success", "data": response})
    
#  Chọn vé và hiển thị giá tiền, lưu data vào session
class SelectTicket(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('flight_id', type=int, required=True, help="Flight Number is required")
    parser.add_argument('seat_class', type=str, required=True, help="Seat class is required")
    parser.add_argument('price', type=float, required=True, help="Price is required")
    parser.add_argument('quantity', type=int, required=True, help="Quantity is required")
    parser.add_argument('trip_type', type=str, required=True, help="Trip type is required")
    
    def format_currency(self, value):
        """Format a number to Vietnamese currency style (e.g., 1.000.000,00)"""
        return f"{value:,.0f}".replace(",", ".")

    def post(self):
        data = self.parser.parse_args()
        flight_id = data['flight_id']
        seat_class = data['seat_class']
        price = data['price']
        quantity = data['quantity']
        trip_type = data['trip_type']
        
        total_price = price * quantity
        vat = total_price * 0.15
        final_price = total_price + vat
        
        ticket_info = {
            'trip_type': trip_type,
            'flight_id': flight_id,
            'seat_class': seat_class,
            'price': price,
            'quantity': quantity,
            'total_price': total_price,
            'vat': vat,
            'final_price': final_price
        }

        # Lưu thông tin vào session
        if 'selected_tickets' not in session:
            session['selected_tickets'] = {}
            
        print("Before session save:", session)
        session['selected_tickets'][trip_type] = ticket_info
        session.modified = True
        print("After session save:", session)

        return {
            "message": f"{trip_type.capitalize()} ticket selected successfully",
            "selected_ticket": ticket_info
        }, 200
                
# Customer xem vé, điền thông tin vé, hủy vé
class TicketCustomer(Resource):
    @jwt_required()
    @authorized_required(roles=["customer"])
    def get(self):
        account_id = get_jwt_identity()
        tickets = Tickets.get_all_ticket_account_id(account_id)
        
        if tickets:
            return tickets
        else:
            return {"message": "Không tìm thấy vé"}, 400
        
    @jwt_required()
    @authorized_required(roles=["customer"])
    def post(self):
        account_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('passengers') or not isinstance(data['passengers'], list):
            print('Invalid or missing passengers data')
            return {"message": "Invalid or missing passengers data"}, 400
        
        trip_type = data.get('trip_type')
        passengers = data['passengers']
        
        if not passengers:
            print('Passengers list is required')
            return {"message": "Passengers list is required"}, 400

        if trip_type not in ["one-way", "round-trip"]:
            print('Invalid trip type')
            return {"message": "Invalid trip type"}, 400
        
        print("Session cookies:", request.cookies)
        print("Session on /ticket-customer:", session)
        
        # Debugging session log
        if 'selected_tickets' in session:
            print("Found session selected_tickets: ", session['selected_tickets'])
        else:
            print("No tickets in session!")

        selected_tickets = session.get('selected_tickets')
        if not selected_tickets:
            print('No selected ticket information found in session')
            return {"message": "No selected ticket information found in session"}, 400
        
        print(f"Selected Tickets: {selected_tickets}")
        
        quantity = selected_tickets.get(trip_type, {}).get('quantity')
        if not quantity:
            print('No quantity information found for the selected trip type')
            return {"message": "No quantity information found for the selected trip type"}, 400

        tickets_created = []  
        for passenger in passengers:
            if trip_type == 'one-way':
                flight_id = selected_tickets['one-way']['flight_id']
                seat_class = selected_tickets['one-way']['seat_class']
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
                    identification=passenger['identification'],
                    family_name=passenger['family_name'],
                    given_name=passenger['given_name'],
                    gender=passenger['gender'],
                    nationality=passenger['nationality'],
                    date_of_birth=passenger['date_of_birth'],
                    phone_number=passenger['phone_number'],
                    email=passenger['email']
                )
                db.session.add(new_ticket_user)
                db.session.commit()

                tickets_created.append(new_ticket)
            elif trip_type == 'round-trip':
                # Tạo vé cho chuyến đi (one-way)
                flight_id_one_way = selected_tickets['one-way']['flight_id']
                seat_class_one_way = selected_tickets['one-way']['seat_class']

                # Tạo vé cho chuyến về (round-trip)
                flight_id_round_trip = selected_tickets['round-trip']['flight_id']
                seat_class_round_trip = selected_tickets['round-trip']['seat_class']

                # Vé cho chuyến đi
                ticket_one_way = Tickets(
                    account_id=account_id,
                    flight_id=flight_id_one_way,
                    ticket_number=TicketS.generate_custom_random_string(),
                    seat_number=None,
                    seat_class=seat_class_one_way,
                        booking_time=datetime.now(),
                        status="scheduled"
                    )
                db.session.add(ticket_one_way)
                db.session.commit()

                new_ticket_user_one_way = TicketUser(
                    ticket_id=ticket_one_way.ticket_id,
                    identification=passenger['identification'],
                    family_name=passenger['family_name'],
                    given_name=passenger['given_name'],
                    gender=passenger['gender'],
                    nationality=passenger['nationality'],
                    date_of_birth=passenger['date_of_birth'],
                    phone_number=passenger['phone_number'],
                    email=passenger['email']
                )
                db.session.add(new_ticket_user_one_way)
                db.session.commit()

                tickets_created.append(ticket_one_way)

                # Vé cho chuyến về
                ticket_round_trip = Tickets(
                    account_id=account_id,
                    flight_id=flight_id_round_trip,
                    ticket_number=TicketS.generate_custom_random_string(),
                    seat_number=None,
                    seat_class=seat_class_round_trip,
                    booking_time=datetime.now(),
                    status="scheduled"
                )
                db.session.add(ticket_round_trip)
                db.session.commit()
                
                new_ticket_user_round_trip = TicketUser(
                    ticket_id=ticket_round_trip.ticket_id,
                    identification=passenger['identification'],
                    family_name=passenger['family_name'],
                    given_name=passenger['given_name'],
                    gender=passenger['gender'],
                    nationality=passenger['nationality'],
                    date_of_birth=passenger['date_of_birth'],
                    phone_number=passenger['phone_number'],
                    email=passenger['email']
                )
                db.session.add(new_ticket_user_round_trip)
                db.session.commit()
                    
                tickets_created.append(ticket_round_trip)

        return {"msg": f"{len(tickets_created)} tickets created successfully"}, 200

    @jwt_required()
    @authorized_required(roles=["customer"])
    def put(self, ticket_id):
        account_id = get_jwt_identity()
        ticket = Tickets.find_ticket_id(ticket_id)
        
        if not ticket:
            print('Ticket not found')
            return {'msg': 'Không tìm thấy vé.'}, 400
        
        if ticket.account_id != account_id:
            return {'msg': 'Không có quyền truy cập.'}, 401
        
        data = request.get_json()
        reason = data.get('reason', '').strip()
        
        if not reason:
            print('Reason is required to cancel the ticket')
            return {'msg': 'Lý do hủy vé là bắt buộc.'}, 400
        
        # Lấy departure_time của chuyến bay
        departure_time = Tickets.find_departure_time(ticket_id)
        print('Departure Time:', departure_time)
        
        if not departure_time:
            return {'msg': 'Không thể tìm thấy thông tin khởi hành.'}, 400
        
        current_date = datetime.now().date()
        departure_date = departure_time
        if departure_date - current_date < timedelta(days=7):
            return {'msg': 'Vé không thể hủy ít hơn 7 ngày trước thời ngày khởi hành'}, 400
        
        ticket.status = StatusClass.cancelled
        db.session.commit()
        
        new_cancellation = Cancellations(
            ticket_id=ticket_id,
            reason=data['reason'],
            cancellation_date=datetime.now()
        )
        new_cancellation.save_to_db()
        
        return {'msg': 'Vé đã được hủy thành công!'}, 200

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
