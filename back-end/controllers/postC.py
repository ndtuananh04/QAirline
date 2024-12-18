import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request
from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from database import db

from models.postsDB import Posts
from services.postS import PostService
from core.auth import authorized_required

class PostDetail(Resource):
    def get(self, post_id):
    
        # Lấy chi tiết một bài post theo ID
        post = Posts.query.get(post_id)
        if post:
            return jsonify(post.to_json_full()) 
        return jsonify({"error": "Post not found"}), 404

# Hiện thông báo
class PostCustomer(Resource):
    def get(self):
        posts = Posts.get_all_posts1()
        
        posts_json = [post.to_json_1() for post in posts]
        
        return jsonify(posts_json)
    
class PostModal(Resource):
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self, post_id):
        post = Posts.get_post_id(post_id)
        if not post:
            return {'msg': 'Bài viết không tìm thấy.'}, 400
        
        return post
    
# Admin quản lý thông báo
class PostAdmin(Resource):
    @jwt_required()
    @authorized_required(roles=["admin"])
    def get(self):
        postsss = Posts.get_all_posts_admin()

        if not postsss:
            return {"msg": "Không có bài viết nào."}, 400
        
        return postsss
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def post(self):
        data = request.get_json()
        title = data['title']
        block_1 = data['block_1']
        block_2 = data['block_2']
        block_3 = data['block_3']
        block_4 = data['block_4']
        block_5 = data['block_5']
        
        if not PostService.is_valid_input(title):
            return {'msg': 'Tiêu đề không hợp lệ.'}, 400
        if not PostService.is_valid_input(block_1):
            return {'msg': 'Block 1 không hợp lệ.'}, 400
        if not PostService.is_valid_input(block_2):
            return {'msg': 'Block 2 không hợp lệ.'}, 400
        if not PostService.is_valid_input(block_3):
            return {'msg': 'Block 3 không hợp lệ.'}, 400
        if not PostService.is_valid_input(block_4):
            return {'msg': 'Block 4 không hợp lệ.'}, 400
        if not PostService.is_valid_input(block_5):
            return {'msg': 'Block 5 không hợp lệ.'}, 400
        
        new_post = Posts(
            title=title,
            block_1=block_1,
            block_2=block_2,
            block_3=block_3,
            block_4=block_4,
            block_5=block_5,
            post_date=datetime.now()
        )
        new_post.save_to_db()
        
        return {'msg': 'Bài viết đã được thêm thành công'}, 201
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def delete(self, post_id):
        post = Posts.query.get(post_id)
        if not post:
            return {'msg': 'Bài viết không tìm thấy.'}, 400
        
        db.session.delete(post)
        db.session.commit()
        
        return {'msg': 'Bài viết đã được xóa thành công'}, 200
    
    @jwt_required()
    @authorized_required(roles=["admin"])
    def put(self, post_id):
        post = Posts.find_post_id(post_id)
        if not post:
            return {'msg': 'Bài viết không tìm thấy.'}, 400

        # Lấy dữ liệu JSON từ yêu cầu
        data = request.get_json()

        # Chỉ cập nhật các trường có trong payload
        if 'title' in data and data['title']:
            post.title = data['title']
        if 'block_1' in data and data['block_1']:
            post.block_1 = data['block_1']
        if 'block_2' in data and data['block_2']:
            post.block_2 = data['block_2']
        if 'block_3' in data and data['block_3']:
            post.block_3 = data['block_3']
        if 'block_4' in data and data['block_4']:
            post.block_4 = data['block_4']
        if 'block_5' in data and data['block_5']:
            post.block_5 = data['block_5']
        post.post_date = datetime.now()

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()

        return {'msg': 'Bài viết đã được cập nhật thành công'}, 200