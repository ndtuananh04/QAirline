from datetime import datetime
from database import db
from sqlalchemy.sql import func
import re

def valid_date(date_str):
    """Kiểm tra định dạng ngày (YYYY-MM-DD)"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in format YYYY-MM-DD")

def valid_time(time_str):
    """Kiểm tra định dạng giờ (HH:MM)"""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        raise ValueError("Time must be in format HH:MM")
    
class FlightService:
    @staticmethod
    def check_flight_number(input_str):
        # Biểu thức chính quy: 3 số + 3 chữ "QAL"
        pattern = r'^[1-9][0-9]{5}QAL$'
        # Kiểm tra nếu đầu vào khớp với biểu thức chính quy
        if re.match(pattern, input_str):
            return True
        else:
            return False
        
    @staticmethod
    def check_location(input_str):
        # Biểu thức chính quy: chỉ cho phép chữ cái (có thể có dấu) và dấu chấm
        pattern = r'^[a-zA-ZÀ-ỹà-ỹ\s\.]+$'
        # Kiểm tra nếu đầu vào khớp với biểu thức chính quy
        if re.match(pattern, input_str):
            return True
        else:
            return False
        
    @staticmethod
    def check_code(input_str):
        # Biểu thức chính quy: chỉ cho phép đúng 3 chữ cái viết hoa không dấu
        pattern = r'^[A-Z]{3}$'
        # Kiểm tra nếu đầu vào khớp với biểu thức chính quy
        if re.match(pattern, input_str):
            return True
        else:
            return False
        