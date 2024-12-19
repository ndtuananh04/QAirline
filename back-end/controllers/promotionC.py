import os
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource, reqparse
from database import db
from flask import jsonify, session, request
from models.promotionsDB import Promotions
from services.promotionS import PromotionService
from core.auth import authorized_required

class PromotionPrice(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('code_promotion', type=str, required=True, help="Code promotion is required")
    parser.add_argument('total_price', type=int, required=True, help="Total price is required")
    def post(self):
        data = self.parser.parse_args()
        code_promotion = data['code_promotion']
        total_price = data['total_price']
        
        # Kiểm tra mã giảm giá
        promotion = Promotions.find_promotion_code(code_promotion)
        if not promotion:
            return jsonify({"message": "Invalid promotion code"}), 404
        
        final_price = total_price - total_price * (promotion.percent / 100)
        return {
            "final_price": final_price,
            "message": "Promotion applied successfully"
        }, 200
        
class PromotionAdmin(Resource):
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):
        promotions = Promotions.get_all_promotions()
        
        return promotions

    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        data = request.get_json()
        code_promotion = data['code_promotion']
        percent = data['percent']
        
        if not PromotionService.validate_input(code_promotion):
            return {"msg": "Mã khuyến mại không hợp lệ."}, 400
        
        if not PromotionService.is_numeric_input(percent):
            return {"msg": "Phần trăm khuyến mại không hợp lệ."}, 400

        if Promotions.find_promotion_code(code_promotion):
            return {"msg": "Mã khuyến mại đã tồn tại."}, 400
        
        new_promotion = Promotions(code_promotion, percent)
        new_promotion.save_to_db()
        return {"msg": "Thêm mã khuyến mại thành công"}, 201
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self, promotion_id):
        promotion = Promotions.find_promotion_id(promotion_id)
        if not promotion:
            return {"msg": "Không tìm thấy mã khuyến mại"}, 404
        
        promotion.delete_from_db()
        
        return {"msg": "Xóa mã khuyến mại thành công"}, 200
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def put(self, promotion_id):
        promotion = Promotions.find_promotion_id(promotion_id)
        if not promotion:
            return jsonify({"message": "Promotion not found"}), 404
        
        data = request.get_json()
        if 'code_promotion' in data and data['code_promotion']:
            if not PromotionService.validate_input(data['code_promotion']):
                return {"msg": "Mã khuyến mại không hợp lệ"}, 400
            promotion.code_promotion = data['code_promotion']
        if 'percent' in data and data['percent']:
            if not PromotionService.is_numeric_input(data['percent']):
                return {"msg": "Phần trăm khuyến mại không hợp lệ"}, 400
            promotion.percent = data['percent']
        promotion.commit_to_db()
        
        return {"msg": "Cập nhật mã khuyến mại thành công"}, 200