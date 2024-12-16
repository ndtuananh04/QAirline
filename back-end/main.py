from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api

from flask_jwt_extended import create_access_token
from models.accountDB import AccountType

from controllers.accountC import AccountLogin, AccountRegister, UserLogoutAccess, Repass, Valid, VerifyToken
from controllers.flightC import DepartureArrival, FlightSearch, FlightAdmin
from controllers.airplaneC import AirplaneSearch
from controllers.ticketC import TicketCustomer, TicketAdmin, SelectTicket
from controllers.promotionC import PromotionPrice, PromotionAdmin
from controllers.postC import PostCustomer, PostAdmin, PostDetail
from controllers.checkinC import CheckinC
from controllers.seatsC import SeatsAirplane, SeatsAdmin
from controllers.adminC import QuantityRole, AddAccount, DeleteAccount
from services.__init__ import init_app
from controllers.__init__ import init_app


app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.config.from_pyfile('core/config.py')
api = Api(app)
init_app(app)
init_app(app)

api.add_resource(AccountLogin, '/login')
api.add_resource(AccountRegister, '/register')
api.add_resource(UserLogoutAccess, '/logout')
api.add_resource(Repass, '/repass')
api.add_resource(Valid, '/valid')
api.add_resource(VerifyToken, '/verify-token')

api.add_resource(QuantityRole, '/quantity-role')
api.add_resource(AddAccount, '/addaccount')
api.add_resource(DeleteAccount, '/deleteaccount', '/deleteaccount/<int:account_id>')

api.add_resource(DepartureArrival, '/departure-arrival')
api.add_resource(FlightSearch, '/flights-search')
api.add_resource(FlightAdmin, '/flights', '/flights/<int:flight_id>')

api.add_resource(AirplaneSearch, '/airplanes', '/airplanes/<int:airplane_id>')

api.add_resource(SelectTicket, '/select-ticket')
api.add_resource(TicketCustomer, '/ticket-customer', '/ticket-customer/<int:ticket_id>')
api.add_resource(TicketAdmin, '/ticket-admin', '/ticket-customer/<int:ticket_id>')

api.add_resource(PromotionPrice, '/promotion-search')
api.add_resource(PromotionAdmin, '/promotions', '/promotions/<int:promotion_id>')

api.add_resource(PostCustomer, '/post-customer')
api.add_resource(PostAdmin, '/post-admin', '/post-admin/<int:post_id>')
api.add_resource(PostDetail, '/post-detail/<int:post_id>')

api.add_resource(CheckinC, '/checkin')

api.add_resource(SeatsAirplane, '/seats-airplane', '/seats-airplane/<int:seat_id>')
api.add_resource(SeatsAdmin, '/seats', '/seats/<int:seat_id>')

def create_database():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    from database import db
    db.init_app(app)
    create_database()
    app.run(debug=True)