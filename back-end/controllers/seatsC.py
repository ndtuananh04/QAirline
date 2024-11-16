import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from flask_restful import Resource, reqparse
from models.accountDB import Account, AccountType
from models.flightDB import  Airplane, Seats
from flask import jsonify
from database import db

class SeatsSearch(Resource):
    parser = reqparse.RequestParser()
    
    