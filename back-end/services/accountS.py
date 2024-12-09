from models.accountDB import Account, AccountType
import re
import random
import string

def validate_regex(input_string, regex):
    """
    Validate input string with a given regular expression
    :param input_string: the string that needed to be checked
    :param regex: regex pattern
    :return: True if satisfy and vice versa
    """
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class AccountS:
    @staticmethod
    def validate_email(email):
        """
        Validate email format
        :param email: email string
        :return: True if valid, False otherwise
        """
        regex_mail = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not validate_regex(email, regex_mail) or len(email) > 320:
            return False
        return True
    
    @staticmethod
    def validate_password(password):
        """
        Validate password format
        :param password: password string
        :return: True if valid, False otherwise
        """
        # At least 8 characters, one uppercase, one lowercase, one number, one special character
        regex_password = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if not validate_regex(password, regex_password):
            return False
        return True
    
    def validate_identification(identification):
        """
        Validate the identification number.
        The identification must:
        - Contain only digits.
        - Have exactly 12 digits.
        :param identification: Identification number to validate.
        :return: True if valid, False otherwise.
        """
        
        identification = str(identification)

        # Regex pattern: chỉ cho phép đúng 12 số
        regex = r'^\d{12}$'
        
        # Kiểm tra với regex
        if re.fullmatch(regex, identification):
            return True
        return False
    
    def validate_phone_number(phone_number):
        """
        Validate the phone number.
        The phone number must:
        - Contain only digits.
        - Have exactly 10 digits.
        :param phone_number: Phone number to validate.
        :return: True if valid, False otherwise.
        """
        
        phone_number = str(phone_number)
        # Regex pattern: chỉ cho phép đúng 10 số
        regex = r'^\d{10}$'
        
        # Kiểm tra với regex
        if re.fullmatch(regex, phone_number):
            return True
        return False
    
    @staticmethod
    def random_string(length = 12):
        """
        Generate a random secure password
        :param length: length of the password
        :return: a secure random password
        """
        if length < 8:  # Minimum length for security
            length = 8
        char_pool = string.ascii_letters + string.digits + "@$!%*?&"
        password = ''.join(random.choice(char_pool) for _ in range(length))
        return password
    
    @classmethod
    def area_name_of_acc(cls, user):
        if user.role == AccountType.admin:
            return "admin"
        elif user.role == AccountType.customer:
            return "customer"
        return ""
