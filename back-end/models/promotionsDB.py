from database import db
from flask import jsonify
from sqlalchemy.sql import func
from collections import OrderedDict

class Promotions(db.Model):
    __tablename__ = 'promotions'
    promotion_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_promotion = db.Column(db.String(10), unique=True, nullable=False)
    percent = db.Column(db.Integer, nullable=False)

    def __init__(self, code_promotion, percent):    
        self.code_promotion = code_promotion
        self.percent = percent
    
    def to_json(self):
        return {
            "promotion_id": self.promotion_id,
            "code_promotion": self.code_promotion,
            "percent": self.percent
        }
    
    @classmethod
    def find_promotion_id(cls, promotion_id):
        return cls.query.filter_by(promotion_id=promotion_id).first()
    
    @classmethod
    def find_promotion_code(cls, code_promotion):
        return cls.query.filter_by(code_promotion=code_promotion).first()
    
    @classmethod
    def get_all_promotions(cls):
        promotions = db.session.query(
            Promotions.promotion_id,
            Promotions.code_promotion,
            Promotions.percent
        ).all()
        
        promotions_list = {}
        for promotion in promotions:
            promotions_list[promotion.promotion_id] = {
                "promotion_id": promotion.promotion_id,
                "code_promotion": promotion.code_promotion,
                "percent": promotion.percent
            }
        results = list(promotions_list.values())
        
        return results
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()