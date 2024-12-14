import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import jsonify, request
from database import db

from flask_restful import Resource, reqparse
from models.accountDB import Account, AccountType
from models.airplanesDB import  Airplanes
from core.auth import authorized_required

class AirplaneSearch(Resource):
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):
        # Tìm kiếm may bay dựa trên tên
        airplanes = Airplanes.get_all_airplanes()
        if not airplanes:
            return {'msg': 'Không có máy bay nào'}, 400
        
        return airplanes
        
    '''Admin thêm airplane mới'''
    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        data = request.get_json()
        name_airplane = data['name_airplane']
        capacity = data['capacity']

        existing_airplane = Airplanes.find_name_airplane(name_airplane)
        if existing_airplane:
            if existing_airplane.is_locked == 0:
                # Nếu đã tồn tại máy bay với `is_locked=0`, không thêm mới
                return {'msg': 'Máy bay đã tồn tại'}, 400
            elif existing_airplane.is_locked == 1:
                existing_airplane.is_locked = 0
            else:
                # Nếu đã tồn tại máy bay với `is_locked=0`, mở khóa và cập nhật capacity
                existing_airplane.is_locked = 0
                existing_airplane.capacity = capacity
                db.session.commit()
        # Nếu không tồn tại máy bay nào, tạo máy bay mới
        new_airplanes = Airplanes(
            name_airplane=data['name_airplane'],
            capacity=capacity,
            is_locked=False
        )
        new_airplanes.save_to_db()
        
        return {'msg': 'Máy bay đã được thêm thành công'}, 201
    
    '''Admin khóa/mở airplane'''    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self, airplane_id):
        airplane = Airplanes.find_airplane_id(airplane_id)
        if not airplane: 
            return {'msg': 'Máy bay không tìm thấy.'}, 400
        
        airplane.is_locked = 0 if airplane.is_locked == 1 else 1

        db.session.commit()

        if airplane.is_locked == 1:
            return {'msg': 'Khóa máy bay thành công.'}, 201
        else:
            return {'msg': 'Mở khóa máy bay thành công.'}, 200
    
    '''Admin cập nhật thông tin airplane'''   
    @jwt_required()
    @authorized_required(roles=["admin"])
    def put(self, airplane_id):  
        data = request.get_json()
        name_airplane = data['name_airplane']
        capacity = data['capacity']

        airplane = Airplanes.find_airplane_id(airplane_id)
        if not airplane:
            return {'msg': 'Không tìm thấy máy bay.'}, 400

        airplane.name_airplane = name_airplane
        airplane.capacity = capacity
        db.session.commit()

        return {'msg': 'Cập nhật máy bay thành công'}, 200