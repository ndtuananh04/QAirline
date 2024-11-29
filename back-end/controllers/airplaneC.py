import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import jsonify
from database import db

from flask_restful import Resource, reqparse
from models.accountDB import Account, AccountType
from models.airplanesDB import  Airplanes
from core.auth import authorized_required

class AirplaneSearch(Resource):
    parser = reqparse.RequestParser()
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):
        # Tìm kiếm may bay dựa trên tên
        airplanes = Airplanes.get_all_airplanes()
        return airplanes
        
    '''Admin thêm airplane mới'''
    airplane_parser = reqparse.RequestParser()
    airplane_parser.add_argument('name_airplane', type=str, required=True, help="Airplane name is required")
    airplane_parser.add_argument('capacity', type=int, required=True, help="Capacity is required")

    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        data = AirplaneSearch.airplane_parser.parse_args()
        name_airplane = data['name_airplane']

        existing_airplane = Airplanes.find_name_airplane(name_airplane)
        if existing_airplane:
            if existing_airplane.is_locked == 0:
                # Nếu đã tồn tại máy bay với `is_locked=0`, không thêm mới
                return {'msg': 'Airplane already exists'}, 400
            elif existing_airplane.is_locked == 1:
                existing_airplane.is_locked = 0
            else:
                # Nếu đã tồn tại máy bay với `is_locked=0`, mở khóa và cập nhật capacity
                existing_airplane.is_locked = 0
                existing_airplane.capacity = data['capacity']
                db.session.commit()
        # Nếu không tồn tại máy bay nào, tạo máy bay mới
        new_airplanes = Airplanes(
            name_airplane=data['name_airplane'],
            capacity=data['capacity'],
            is_locked=False
        )
        new_airplanes.save_to_db()
        new_airplanes = Airplanes.get_all_airplanes()
        return new_airplanes
    
    '''Admin xóa airplane'''    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self, airplane_id):
        airplane = Airplanes.find_name_airplane_with_locked(airplane_id)
        if not airplane: 
            return {'msg': 'Airplane not found'}, 400

        airplane.is_locked = 1
        db.session.commit()

        return {'msg': 'Airplane deleted successfully'}, 200
    
    '''Admin cập nhật thông tin airplane'''
    update_parser = reqparse.RequestParser()
    update_parser.add_argument('name_airplane', type=str, required=True, help="Airplane name is required")
    update_parser.add_argument('capacity', type=int, required=True, help="Capacity is required")
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def put(self):
        # Kiểm tra quyền quản trị
        current_user = get_jwt_identity()
        account = Account.find_account_id(current_user['account_id'])

        if not account:
            return {'msg': 'Account not found'}, 400
        
        data = AirplaneSearch.update_parser.parse_args()
        name_airplane = data['name_airplane']

        airplane = Airplanes.find_name_airplane(name_airplane)
        if not airplane:
            return {'msg': 'Airplane not found'}, 400

        # Nếu máy bay bị khóa, chuyển is_locked thành False và cập nhật thông tin
        if not airplane.is_locked:
            airplane.is_locked = False
            airplane.name_airplane = data['name_airplane']
            airplane.capacity = data['capacity']
            db.session.commit()
            return {'msg': 'Airplane unlocked and updated successfully'}, 200

        # Nếu máy bay không bị khóa, chỉ cần cập nhật name_airplane và capacity
        airplane.name_airplane = data['name_airplane']
        airplane.capacity = data['capacity']
        db.session.commit()

        return {'msg': 'Airplane updated successfully'}, 200