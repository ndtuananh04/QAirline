from datetime import datetime

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