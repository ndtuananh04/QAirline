import os
from flask_restful import Resource, reqparse
from models.accountDB import AccountDB, UserInfo
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_mail import Message
from services.accountS import AccountS
from database import db

class AccountLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    def get(self):
        pass

    def post(self):
        data  = AccountLogin.parser.parse_args()
        email = data['email']
        password = data['password']  

        if not AccountS.validate_input_email_pass(email, password):
            return {'msg': "Invalid id or password"}, 400
        
        user = AccountDB.find_email(email)

        if user is None:
            return {'msg': "Incorrect email or password"}, 401
        
        name = AccountS.area_name_of_acc(user)

        if check_password_hash(user.password, password):
            additional_claim = {"role": user.role, "name": name}
            access_token = create_access_token(email=email, additional_claims=additional_claim)

            # Trả về token cho frontend
            try:
                return jsonify(access_token=access_token.decode('utf-8'))
            except:
                return jsonify(access_token=access_token)
        
        return {"msg": "Incorrect username or password"}, 401
    
    def delete(self):
        return {'msg': 'Not allowed'}, 404

    def put(self):
        return {'msg': 'Not allowed'}, 404
    
class AccountRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    parser.add_argument('identification', type=int, required=True, help="This field cannot be left blank")
    parser.add_argument('family_name', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('given_name', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('gender', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('nationality', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('date_of_birth', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('phone_number', type=str, required=True, help="This field cannot be left blank")

    def get(self):
        pass

    def post(self):
        data = AccountRegister.parser.parse_args()
        email = data['email']
        password = data['password']
        identification = data['identification']
        phone_number = data['phone_number']

        # Kiểm tra xem email đã tồn tại chưa
        if AccountDB.find_email(email):
            return {'msg': "Email already exists"}, 400

        # Kiểm tra xem identification đã tồn tại trong bảng user_infor chưa
        if UserInfo.query.filter_by(identification=identification).first():
            return {'msg': "Identification already exists"}, 400

        if UserInfo.query.filter_by(phone_number=phone_number).first():
            return {'msg': "Phone already exists"}, 400

        # Mã hóa mật khẩu
        hashed_password = generate_password_hash(password)

        # Tạo tài khoản mới trong bảng account
        new_account = AccountDB(email=email, password=hashed_password, role=2)
        db.session.add(new_account)
        db.session.commit()

        # Tạo bản ghi mới trong bảng user_infor với identification tùy ý
        new_user_info = UserInfo(
            identification=identification,
            family_name=data['family_name'],
            given_name=data['given_name'],
            gender=data['gender'],
            nationality=data['nationality'],
            date_of_birth=data['date_of_birth'],
            phone_number=data['phone_number']
        )
        db.session.add(new_user_info)
        db.session.commit()

        return {"msg": "Account created successfully"}, 201