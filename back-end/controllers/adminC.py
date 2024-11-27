from models.accountDB import *
from flask_restful import Resource, reqparse
from flask import jsonify
from models.accountDB import Account
from werkzeug.security import generate_password_hash
from database import AlchemyEncoder
import json
from models.accountDB import AccountType
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

def getUsers():
    accounts = Account.query.with_entities(Account.account_id, 
                                           Account.email, 
                                           Account.password, 
                                           Account.role).all()
    
    accounts_json = json.dumps(accounts, cls=AlchemyEncoder)

    return jsonify({"accounts": accounts_json})

class AddAccount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    @jwt_required()
    def get(self):
        return getUsers()
    
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        account = Account.find_account_id(current_user_id)

        if not account:
            return {'msg': 'Account not found'}, 400
        
        if account.role != AccountType.admin:
            return {'msg': 'Access forbidden: Only admins can add accounts'}, 400

        data  = AddAccount.parser.parse_args()
        email = data['email']
        password = data['password']

        if Account.find_email(email):
            return {'msg': "Email already exists"}, 400
        
        hashed_password = generate_password_hash(password)

        new_account = Account(email=email, password=hashed_password, role=AccountType.admin)
        new_account.save_to_db()

        #Cập nhật lại panel sau khi add
        return getUsers()
    
class DeleteAccount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")

    @jwt_required()
    def get():
        return getUsers()
    
    @jwt_required()
    def post():

        current_user_id = get_jwt_identity()
        account = Account.find_account_id(current_user_id)

        if not account:
            return {'msg': 'Account not found'}, 400
        
        if account.role != AccountType.admin:
            return {'msg': 'Access forbidden: Only admins can delete accounts'}, 400
        
        data = DeleteAccount.parser.parse_args()
        email = data['email']
        user = Account.find_email(email)
        user.delete_from_db()

class EditAccount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('account_id', type=int, required=True, help="This field cannot be left blank")
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    @jwt_required()
    def get(self):
        return getUsers()
    
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        account = Account.find_account_id(current_user_id)

        if not account:
            return {'msg': 'Account not found'}, 400
        
        if account.role != AccountType.admin:
            return {'msg': 'Access forbidden: Only admins can add accounts'}, 400
        

        data = EditAccount.parser.parse_args()
        account_id = data['account_id']
        email = data['email']
        password = data['password']

        user = Account.find_account_id(account_id)
        user.email = email
        user.password = generate_password_hash(password)
        db.session.commit()
        return getUsers()

    





