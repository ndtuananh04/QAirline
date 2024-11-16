from models.accountDB import *
from flask_restful import Resource, reqparse
from flask import jsonify
from models.accountDB import Account
from werkzeug.security import generate_password_hash


class AddAccount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    def get():
        return getUsers()
    
    def post():
        data  = AddAccount.parser.parse_args()
        email = data['email']
        password = data['password']

        if Account.find_email(email):
            return {'msg': "Email already exists"}, 400
        
        hashed_password = generate_password_hash(password)

        new_account = Account(email=email, password=hashed_password, role=1)
        new_account.save_to_db()

        #Cập nhật lại panel sau khi add
        return getUsers()
    
class DeleteAccount(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")

    def get():
        return getUsers()
    
    def post():
        data = DeleteAccount.parser.parse_args()
        email = data['email']
        user = Account.find_email(email)
        user.delete_from_db()
        
    

def getUsers():
    accounts = Account.query.all()
    return (jsonify({'accounts': accounts}), 200)



