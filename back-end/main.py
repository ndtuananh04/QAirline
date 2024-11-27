from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api

from flask_jwt_extended import create_access_token
from models.accountDB import AccountType

from controllers.accountC import AccountLogin, AccountRegister, UserLogoutAccess, Repass
from controllers.flightC import DepartureArrival
from services.__init__ import init_app
from controllers.__init__ import init_app
from controllers.adminC import *
from controllers.flightC import FlightSearch

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
api.add_resource(DepartureArrival, '/departure-arrival')
api.add_resource(FlightSearch, '/flight-search')

api.add_resource(AddAccount, '/addaccount')
api.add_resource(DeleteAccount, '/deleteaccount')

def create_database():
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    from database import db
    db.init_app(app)
    create_database()
    app.run(debug=True)