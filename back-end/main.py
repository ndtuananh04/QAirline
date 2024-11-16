from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api

from controllers.accountC import AccountLogin, AccountRegister, UserLogoutAccess, Repass
from controllers.flightC import FlightSearch
from controllers.ticketC import TicketSearch
from controllers.airplaneC import AirplaneSearch
from services.__init__ import init_app
from controllers.__init__ import init_app

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

api.add_resource(FlightSearch, '/flightSearch', 'flightSearch/<string:flight_id>')

api.add_resource(TicketSearch, '/ticketSearch', 'ticketSearch/<string:ticket_id>')

api.add_resource(AirplaneSearch, '/airplaneSearch', 'airplaneSearch/<string:airplane_id>')

if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run(debug=True)