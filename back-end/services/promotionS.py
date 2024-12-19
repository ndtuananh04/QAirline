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
    
    @staticmethod
    def is_numeric_input(input_string):
        """
        Kiểm tra nếu input_string chỉ chứa các ký tự số.
        :param input_string: Chuỗi cần kiểm tra
        :return: True nếu chỉ toàn số, False nếu không
        """
        # Kiểm tra bằng biểu thức chính quy
        return bool(re.fullmatch(r'\d+', str(input_string)))
    
    @staticmethod
    def validate_input(input_string):
        """
        Kiểm tra xem đầu vào có thỏa mãn các điều kiện:
        - Độ dài 8 ký tự.
        - Có ít nhất 1 ký tự là chữ in hoa.
        - Có ít nhất 1 chữ số.
        - Chỉ chứa các chữ cái không dấu và chữ số.

        Args:
            input_string (str): Chuỗi cần kiểm tra.

        Returns:
            bool: True nếu chuỗi thỏa mãn các điều kiện, False nếu không.
        """
        pattern = r"^(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8}$"
        return bool(re.fullmatch(pattern, input_string))