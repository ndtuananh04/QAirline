import os
from flask_restful import Resource, reqparse
from models.accountDB import Account, RevokedTokenModel
from models.userInfoDB import UserInfo
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_mail import Message
from services.accountS import AccountS
from database import db
from services import my_mail
from datetime import timedelta
import random
from itsdangerous import URLSafeTimedSerializer

class AccountLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    def get(self):
        pass

    def post(self):
        data = AccountLogin.parser.parse_args()
        email = data['email']
        password = data['password']  
        
        if not AccountS.validate_email(email):
            print("Email không hợp lệ. Vui lòng kiểm tra và thử lại.")
            return {'msg': "Email không hợp lệ. Vui lòng kiểm tra và thử lại."}, 400
        
        if not AccountS.validate_password(password):
            print("Mật khẩu phải tối thiểu 8 ký tự phải có ít nhất 1 chữ hoa, 1 ký tự đặc biệt, 1 số")
            return {'msg': "Mật khẩu phải tối thiểu 8 ký tự phải có ít nhất 1 chữ hoa, 1 ký tự đặc biệt, 1 số"}, 400

        # Tìm tài khoản theo email
        user = Account.find_email(email)

        if user is None:
            return {'msg': "Tên người dùng hoặc mật khẩu không chính xác."}, 400
        name = AccountS.area_name_of_acc(user)

        # Kiểm tra mật khẩu
        if check_password_hash(user.password, password):
            additional_claim = {"role": user.role.name, "name": name}
            access_token = create_access_token(identity=user.account_id, additional_claims=additional_claim)

            # return jwt to FE
            try:
                return jsonify(access_token=access_token)
            except:
                return jsonify(access_token=access_token)

        return {"msg": "Tên người dùng hoặc mật khẩu không chính xác."}, 401
    
    def delete(self):
        return {'msg': 'Not allowed'}, 404

    def put(self):
        return {'msg': 'Not allowed'}, 404
    
class AccountRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank")

    parser.add_argument('identification', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('family_name', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('given_name', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('gender', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('nationality', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('date_of_birth', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('phone_number', type=str, required=True, help="This field cannot be left blank")

    def get(self):
        pass

    def post(self):
        data = self.parser.parse_args()
        email = data['email']
        password = data['password']
        identification = data['identification']
        phone_number = data['phone_number']
        print(f"Received identification: {identification}, Type: {type(identification)}")
        
        if not AccountS.validate_email(email):
            print("Email không hợp lệ. Vui lòng kiểm tra và thử lại.")
            return {'msg': "Email không hợp lệ. Vui lòng kiểm tra và thử lại."}, 400
        
        if not AccountS.validate_password(password):
            print("Mật khẩu phải tối thiểu 8 ký tự phải có ít nhất 1 chữ hoa, 1 ký tự đặc biệt, 1 số")
            return {'msg': "Mật khẩu phải tối thiểu 8 ký tự phải có ít nhất 1 chữ hoa, 1 ký tự đặc biệt, 1 số"}, 400
        
        if not AccountS.validate_identification(identification):
            print("Số chứng minh nhân dân phải đúng 12 số")
            return {'msg': "Số chứng minh nhân dân phải đúng 12 số"}, 400
        
        if not AccountS.validate_phone_number(phone_number):
            print("Số điện thoại phải đúng 10 số")
            return {'msg': "Số điện thoại phải đúng 10 số"}, 400

        # Kiểm tra xem email đã tồn tại chưa
        if Account.find_email(email):
            print("Email đã tồn tại.")
            return {'msg': "Email đã tồn tại."}, 400

        # Kiểm tra xem identification đã tồn tại trong bảng user_infor chưa
        if UserInfo.query.filter_by(identification=identification).first():
            return {'msg': "CMND/CCCD đã tồn tại."}, 400

        if UserInfo.query.filter_by(phone_number=phone_number).first():
            return {'msg': "Số điện thoại đã tồn tại"}, 400

        # Mã hóa mật khẩu
        hashed_password = generate_password_hash(password)

        # Tạo tài khoản mới trong bảng account
        new_account = Account(email=email, password=hashed_password, role='customer')
        db.session.add(new_account)
        db.session.commit()

        # Tạo bản ghi mới trong bảng user_infor với identification tùy ý
        new_user_info = UserInfo(
            account_id=new_account.account_id,
            identification=data['identification'],
            family_name=data['family_name'],
            given_name=data['given_name'],
            gender=data['gender'],
            nationality=data['nationality'],
            date_of_birth=data['date_of_birth'],
            phone_number=data['phone_number']
        )
        db.session.add(new_user_info)
        db.session.commit()

        return {"msg": "Đăng ký tài khoản thành công!"}, 200
    
class VerifyToken(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user = Account.query.filter_by(account_id=current_user).first()
        if user:
            user_info = UserInfo.query.filter_by(account_id=user.account_id).first()
            if user_info:
                return jsonify(
                    user_email=user.email,
                    family_name=user_info.family_name,
                    given_name=user_info.given_name
                )
        return {'msg': 'Token is invalid'}, 401
    
class UserLogoutAccess(Resource):
    """
    User Logout Api
    """

    @jwt_required()
    def post(self):

        jti = get_jwt()['jti']
        try:
            # Revoking access token
            revoked_token = RevokedTokenModel(jti=jti)

            revoked_token.add()

            return {'msg': 'Access token has been revoked'}, 200

        except:
            return {'msg': 'Something went wrong'}, 500
        
class Repass(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)

    @jwt_required() 
    def post(self):
        data = Repass.parser.parse_args()
        email = data['email']

        if not AccountS.validate_email(email):
            return {'msg': "Check your Email or Password"}, 400

        get_user = Account.find_email(email)
        
        if get_user is None:
            return {'msg': "No account with this Email"}, 400
        try:
            new_password = AccountS.random_string()
            # Gửi new password qua email
            get_user.password = generate_password_hash(new_password, method='sha256')
            msg = Message('New Password Recovery', sender=os.environ.get('MAIL'), recipients=[email.lower()])
            msg.body = 'Your new password is {}'.format(new_password)
            my_mail.send(msg)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'msg': "Unable to send confirmation mail"}, 400
        return {'msg': "New password sent to your mailbox!"}, 200