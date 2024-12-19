import re

class PostService:
    @staticmethod
    def is_valid_input(data):
        # Biểu thức chính quy cho phép chữ cái, số, dấu chấm, dấu phẩy, dấu chấm than, dấu hỏi, dấu "/" và khoảng cách
        pattern = r'^[a-zA-ZÀ-ỿ0-9.,!?/ "\'()*&^%$#@!+=\-_]*$'
        
        # Kiểm tra nếu dữ liệu khớp với biểu thức chính quy
        if re.match(pattern, data):
            return True
        return False