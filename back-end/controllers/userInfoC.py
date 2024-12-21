import os
from flask import session, redirect, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse
from database import db
from core.auth import authorized_required
from models.userInfoDB import UserInfo
from models.accountDB import Account

class UserInfoController(Resource):
    @jwt_required()
    @authorized_required(roles=["customer"])
    def get(self):
        user_id = get_jwt_identity()
        user = UserInfo.find_user_id(user_id)
        
        if user is None:
            return {"msg": "Không tìm thấy thông tin người dùng"}, 404
        
        return user
    
    @jwt_required()
    @authorized_required(roles=["customer"])
    def put(self):
        account_id = get_jwt_identity()
        account = Account.find_account_id(account_id)
        if account is None:
            return {"msg": "Không tìm thấy tài khoản người dùng"}, 404
        
        user_info = UserInfo.find_by_account_id(account_id)
        if user_info is None:
            return {"msg": "Không tìm thấy thông tin người dùng"}, 404
        
        data = request.get_json()
        
        if 'identification' in data and data['identification']:
            user_info.identification = data['identification']
        if 'family_name' in data and data['family_name']:
            user_info.family_name = data['family_name']
        if 'given_name' in data and data['given_name']: 
            user_info.given_name = data['given_name']
        if 'gender' in data and data['gender']:
            user_info.gendet = data['gender']
        if 'nationality' in data and  data['nationality']:
            user_info.nationality = data['nationality']
        if 'date_of_birth' in data and data['date_of_birth']:
            user_info.date_of_birth = data['date_of_birth']
        if 'phone_number' in data and data['phone_number']:
            user_info.phone_number = data['phone_number']
        if 'email' in data and data['email']:
            account.email = data['email']
            
        db.session.commit()
        return {"msg": "Cập nhật thông tin người dùng thành công"}, 200
            