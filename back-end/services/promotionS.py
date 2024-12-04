from models.accountDB import Account
import re
import random
import string

class PromotionService:
    def generate_custom_random_string():
        # Chọn ít nhất 3 ký tự là chữ cái in hoa
        upper_case_chars = random.sample(string.ascii_uppercase, 3)
        
        # Chọn 3 ký tự còn lại ngẫu nhiên từ chữ cái in hoa và số
        other_chars = random.choices(string.ascii_uppercase + string.digits, k=3)
        
        # Ghép 2 phần lại và xáo trộn để đảm bảo tính ngẫu nhiên
        random_string = upper_case_chars + other_chars
        random.shuffle(random_string)
        
        # Trả về chuỗi sau khi ghép
        return ''.join(random_string)