import os
from flask_restful import Resource, reqparse
from models.accountDB import Account, UserInfo, RevokedTokenModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_mail import Message
from services.accountS import AccountS
from database import db
from services import my_mail

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
        
        user = Account.find_email(email)

        if user is None:
            return {'msg': "Incorrect email or password"}, 401
        
        name = AccountS.area_name_of_acc(user)

        if check_password_hash(user.password, password):
            additional_claim = {"role": user.role, "name": name}
            access_token = create_access_token(email=email, additional_claims=additional_claim)
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
        if Account.find_email(email):
            return {'msg': "Email already exists"}, 400

        # Kiểm tra xem identification đã tồn tại trong bảng user_infor chưa
        if UserInfo.query.filter_by(identification=identification).first():
            return {'msg': "Identification already exists"}, 400

        if UserInfo.query.filter_by(phone_number=phone_number).first():
            return {'msg': "Phone already exists"}, 400

        # Mã hóa mật khẩu
        hashed_password = generate_password_hash(password)

        # Tạo tài khoản mới trong bảng account
        new_account = Account(email=email, password=hashed_password, role=2)
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