from models.accountDB import *
from flask_restful import Resource, reqparse
from flask import jsonify
from models.accountDB import Account
from werkzeug.security import generate_password_hash
from database import AlchemyEncoder
import json
from models.accountDB import AccountType
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from core.auth import authorized_required

def getUsers():
    accounts = Account.query.with_entities(Account.account_id, 
                                           Account.email, 
                                           Account.password, 
                                           Account.role).all()
    
    accounts_json = json.dumps(accounts, cls=AlchemyEncoder)

    return json.loads(accounts_json)

class AddAccount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    @jwt_required()
    def get(self):
        return getUsers()
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        current_user_id = get_jwt_identity()
        account = Account.find_account_id(current_user_id)

        if not account:
            return {'msg': 'Account not found'}, 400

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
    parser.add_argument('account_id', type=str, required=True, help="This field cannot be left blank")

    @jwt_required()
    def get(self):
        return getUsers()
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self):
        current_user_id = get_jwt_identity()
        account = Account.find_account_id(current_user_id)

        if not account:
            return {'msg': 'Account not found'}, 400
        
        data = DeleteAccount.parser.parse_args()
        account_id = data['account_id']
        user = Account.find_account_id(account_id)
        user.delete_from_db()
        return getUsers()

class UpdateAccount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('account_id', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        current_user_id = get_jwt_identity()
        account = Account.find_account_id(current_user_id)

        if not account:
            return {'msg': 'Account not found'}, 400
        
        data = UpdateAccount.parser.parse_args()
        selected = Account.find_account_id(data['account_id'])
        if not selected:
            return jsonify({'msg':'No such account!'}), 404
        selected.email = data['email']
        selected.password = generate_password_hash(data['password'])
        selected.commit_to_db()
        return getUsers()
