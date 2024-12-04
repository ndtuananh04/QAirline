from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api

from flask_jwt_extended import create_access_token
from models.accountDB import AccountType

from controllers.accountC import AccountLogin, AccountRegister, UserLogoutAccess, Repass
from controllers.flightC import DepartureArrival, FlightSearch, FlightAdmin
from controllers.airplaneC import AirplaneSearch
from controllers.ticketC import TicketCustomer, TicketAdmin
from services.__init__ import init_app
from controllers.__init__ import init_app
from controllers.adminC import *


app = Flask(__name__)
CORS(app)
app.config.from_pyfile('core/config.py')
api = Api(app)
init_app(app)
init_app(app)

api.add_resource(AccountLogin, '/login')
api.add_resource(AccountRegister, '/register')
api.add_resource(UserLogoutAccess, '/logout')
api.add_resource(Repass, '/repass')

api.add_resource(AddAccount, '/addaccount')
api.add_resource(DeleteAccount, '/deleteaccount')

api.add_resource(DepartureArrival, '/departure-arrival')
api.add_resource(FlightSearch, '/flights-search')
api.add_resource(FlightAdmin, '/flights', '/flights/<int:flight_id>')

api.add_resource(AirplaneSearch, '/airplanes', '/airplanes/<int:airplane_id>')

api.add_resource(TicketCustomer, '/ticket-customer', '/ticket-customer/<int:ticket_id>')

def create_database():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    from database import db
    db.init_app(app)
    create_database()
    with app.app_context():
        additional_claim = {"role": AccountType.admin.name, "name": "admin"}
        access_token = create_access_token(identity=16, additional_claims=additional_claim)
        print(access_token)
    app.run(debug=True)