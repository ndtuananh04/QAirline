import re

class SeatService:
    def validate_seat_number(input_string):
        """
        Kiểm tra chuỗi đầu vào:
        - Độ dài từ 2-3 ký tự.
        - Ký tự cuối cùng là một trong các chữ in hoa A, B, C, D, E, F.
        
        :param input_string: Chuỗi cần kiểm tra.
        :return: True nếu hợp lệ, ngược lại False.
        """
        # Biểu thức chính quy: từ 2 đến 21 ký tự bất kỳ, kết thúc bằng A-F
        pattern = r'^.{1,2}[A-F]$'
        
        if re.fullmatch(pattern, input_string):
            return True
        return False