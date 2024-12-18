from datetime import datetime
from database import db
from sqlalchemy.sql import func

class Posts(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
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
    
    def to_json_2(self):
        return {
            "post_id": self.post_id,
            "title": self.title
        }

    @classmethod
    def get_all_posts_admin(cls):
        posts = db.session.query(
            Posts.post_id,
            Posts.title
        ).all()
        
        posts_list = {}
        
        for post in posts:
            if post.post_id not in posts_list:
                posts_list[post.post_id] = {
                    "post_id": post.post_id,
                    "title": post.title
                }
            results = list(posts_list.values())
        return results
        
    
    @classmethod
    def get_all_posts1(cls):
        return cls.query.all()   
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def commit_to_db(self):
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()