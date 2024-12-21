from datetime import datetime
from database import db
from sqlalchemy.sql import func
import re

class AirplaneService:
    @staticmethod
    def check_format(input_str):
        # Biểu thức chính quy: 3 số + 3 chữ "QAL"
        pattern = r'^[1-9][0-9]{2}QAL$'
        # Kiểm tra nếu đầu vào khớp với biểu thức chính quy
        if re.match(pattern, input_str):
            return True
        else:
            return False
        
    @staticmethod
    def check_positive_integer(input_value):
        # Kiểm tra nếu đầu vào là số nguyên dương
        if isinstance(input_value, int) and input_value > 0:
            return True
        else:
            return False