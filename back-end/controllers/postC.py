import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request
from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from database import db

from models.postsDB import Posts
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
    
# Admin quản lý thông báo
class PostAdmin(Resource):
    @jwt_required
    @authorized_required(roles=["admin"])
    def get(self):
        postsss = Posts.get_all_posts_admin()

        if not postsss:
            return jsonify({"msg": "Không có bài viết nào."}), 400
        
        return postsss