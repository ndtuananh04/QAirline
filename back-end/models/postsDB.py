from datetime import datetime
from database import db
from sqlalchemy.sql import func

class Posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(1024), nullable=False)
    block_1 = db.Column(db.Text, nullable=False)
    block_2 = db.Column(db.Text, nullable=True)
    block_3 = db.Column(db.Text, nullable=True)
    block_4 = db.Column(db.Text, nullable=True)
    block_5 = db.Column(db.Text, nullable=True)
    post_date = db.Column(db.Date, nullable=False)
    
    def __init__(self, title, block_1, block_2, block_3, block_4, block_5, post_date):
        self.title = title
        self.block_1 = block_1
        self.block_2 = block_2
        self.block_3 = block_3
        self.block_4 = block_4
        self.block_5 = block_5
        self.post_date = post_date
        
    def to_json(self):
        return {
            "post_id": self.post_id,
            "title": self.title,
            "block_1": self.block_1,
            "block_2": self.block_2,
            "block_3": self.block_3,
            "block_4": self.block_4,
            "block_5": self.block_5,
            "post_date": self.post_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        
    def to_json_1(self):
        return {
            "post_id": self.post_id,
            "title": self.title,
            "block_1": self.block_1,
            "post_date": self.post_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        
    # Phương thức trả về thông tin chi tiết
    def to_json_full(self):
        return {
            "post_id": self.post_id,
            "title": self.title,
            "block_1": self.block_1,
            "block_2": self.block_2 or '',  # Nếu block_2 null thì sẽ trả về chuỗi rỗng
            "block_3": self.block_3 or '',
            "block_4": self.block_4 or '',
            "block_5": self.block_5 or '',
            "post_date": self.post_date.strftime('%Y-%m-%d %H:%M:%S')
        }    

    @classmethod
    def get_all_posts_admin(cls):
        postsss = db.session.query(
            Posts.post_id,
            Posts.title
        ).all()
        
        posts_list = {}
        
        for post in postsss:
            if post.post_id not in posts_list:
                posts_list[post.post_id] = {
                    "post_id": post.post_id,
                    "title": post.title
                }
            results = list(posts_list.values())
        return results
    
    @classmethod
    def get_post_id(cls, post_id):
        post = db.session.query(
            Posts.post_id,
            Posts.title,
            Posts.block_1,
            Posts.block_2,
            Posts.block_3,
            Posts.block_4,
            Posts.block_5,
        ).filter(Posts.post_id == post_id).first()
        
        post_data = {
            'post_id': post.post_id,
            'title': post.title,
            'block_1': post.block_1,
            'block_2': post.block_2,
            'block_3': post.block_3,
            'block_4': post.block_4,
            'block_5': post.block_5
        }
        
        return post_data
        
    
    @classmethod
    def get_all_posts1(cls):
        return cls.query.all()   
    
    @classmethod
    def find_post_id(cls, post_id):
        return cls.query.filter_by(post_id=post_id).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()