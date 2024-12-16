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
    
    parser = reqparse.RequestParser()
    parser.add_argument('percent', type=int, required=True, help="Percent is required")

    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        data = self.parser.parse_args()
        percent = data['percent']

        # Tạo mã giảm giá
        code_promotion = PromotionService.generate_custom_random_string()
        while Promotions.find_promotion_code(code_promotion):
            code_promotion = PromotionService.generate_custom_random_string()
        
        new_promotion = Promotions(code_promotion, percent)
        new_promotion.save_to_db()
        new_promotions = Promotions.get_all_promotions()
        
        return new_promotions
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self, promotion_id):
        promotion = Promotions.find_promotion_id(promotion_id)
        if not promotion:
            return jsonify({"message": "Promotion not found"}), 404
        
        promotion.delete_from_db()
        new_promotions = Promotions.get_all_promotions()
        return new_promotions