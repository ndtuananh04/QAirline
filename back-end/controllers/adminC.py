from flask import jsonify, session, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from models.userInfoDB import UserInfo
from models.accountDB import Account, AccountType
from core.auth import authorized_required


class QuantityRole(Resource):
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):
        quantity = Account.get_quantity_role()
        return {'admin': quantity['admin'], 'customer': quantity['customer']}, 200

class AddAccount(Resource):
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):        
        accounts = Account.get_all_accounts()
        
        if not accounts:
            return {'msg': 'Không có tài khoản nào'}, 400
        
        return accounts

    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        current_user_id = get_jwt_identity()
        account = Account.find_account_id(current_user_id)

        if not account:
            return {'msg': 'Không tìm thấy tài khoản'}, 400

        data = request.get_json()
        email = data['email']
        password = data['password']

        if Account.find_email(email):
            return {'msg': "Email đã tồn tại"}, 400
        
        hashed_password = generate_password_hash(password)

        new_account = Account(email=email, password=hashed_password, role=AccountType.admin)
        new_account.save_to_db()

        return {'msg': "Tạo tài khoản admin thành công."}, 200
    
class DeleteAccount(Resource):
    @jwt_required()
    @authorized_required(roles=["admin"])
    def put(self, account_id):
        account = Account.find_account_id(account_id)

        if not account:
            return {'msg': 'Không tìm thấy tài khoản'}, 400
        
        data = request.get_json()
        role = data['role']
        if not role:
            return {'msg': 'Vui lòng nhập role'}, 400
        
        account.role = role
        account.commit_to_db()
        return {'msg': "Cập nhật tài khoản thành công."}, 200
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self, account_id):
        account = Account.find_account_id(account_id)

        if not account:
            return {'msg': 'Không tìm thấy tài khoản'}, 400
        
        user_jnfos = UserInfo.find_by_account_id(account_id)
        if user_jnfos:
            user_jnfos.delete_from_db()
        
        account.delete_from_db()
        return {'msg': "Xóa tài khoản thành công."}, 200
