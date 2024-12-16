import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from database import db
from flask import jsonify, request
from models.postsDB import Posts
from core.auth import authorized_required

class PostDetail(Resource):
    def get(self, post_id):
    
        # Lấy chi tiết một bài post theo ID
        post = Posts.query.get(post_id)
        if post:
            return jsonify(post.to_json_full())  # Trả về thông tin chi tiết bài post
        return jsonify({"error": "Post not found"}), 404

# Hiện thông báo
class PostCustomer(Resource):
    def get(self):
        # Lấy danh sách thông báo
        posts = Posts.get_all_posts()
        
        # Dùng list comprehension để chuyển danh sách thành JSON serializable
        posts_json = [post.to_json_1() for post in posts]
        
        # Trả về thông tin JSON
        return jsonify(posts_json)
    
# Admin quản lý thông báo
class PostAdmin(Resource):
    # Hiện tất cả thông báo cho admin
    @jwt_required
    @authorized_required(roles=["admin"])
    def get(self):
         # Lấy danh sách thông báo
        posts = Posts.get_all_posts()
        
        # Dùng list comprehension để chuyển danh sách thành JSON serializable
        posts_json = [post.to_json() for post in posts]
        
        # Trả về thông tin JSON
        return jsonify(posts_json)
    
    #Admin tạo thông báo
    @jwt_required
    @authorized_required(roles=["admin"])
    def post(self):
        data = request.get_json()
        post = Posts(
            title=data["title"],
            block_1=data["block_1"],
            block_2=data["block_2"],
            block_3=data["block_3"],
            block_4=data["block_4"],
            block_5=data["block_5"],
            post_date=datetime.now()
        )
        post.save_to_db()
        
        return jsonify(post.to_json())
    
    # Admin xóa thông báo
    @jwt_required
    @authorized_required(roles=["admin"])
    def delete(self, post_id):
        data = request.get_json()
        post = Posts.query.filter_by(post_id=post_id).first()
        if not post:
            print("Post not found.")
            return jsonify({"message": "Post not found."}), 404
        post.delete_from_db()
        return jsonify({"msg": "Post deleted successfully."})
    
    # Admin sửa thông báo
    @jwt_required
    @authorized_required(roles=["admin"])
    def put(self, post_id):
        data = request.get_json()
        if not data.get("block_1"):
            return jsonify({"msg": "block_1 is required."}), 400
        
        post = Posts.query.filter_by(post_id=post_id).first()
        
        if not post:
            print("Post not found.")
            return jsonify({"message": "Post not found."}), 404
        
        post.title = data["title"]
        post.block_1 = data["block_1"]
        post.block_2 = data.get("block_2", post.block_2) # Nếu không có block_2 thì giữ nguyên block_2 cũ
        post.block_3 = data.get("block_3", post.block_3)
        post.block_4 = data.get("block_4", post.block_4)
        post.block_5 = data.get("block_5", post.block_5)
        post.post_date = datetime.now()
        
        post.save_to_db()
        
        return jsonify({"msg": "Post updated successfully."})
    