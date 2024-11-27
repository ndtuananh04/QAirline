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
        regex_mail = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not validate_regex(email, regex_mail):
            return False
        return True
    
    @staticmethod
    def validate_password(password):
        regex_password = '^[a-z0-9@]*$'
        if not validate_regex(password, regex_password):
            return False
        return True
    
    @staticmethod
    def validate_input_email_pass(email, password):
        if AccountS.validate_email(email):
            return False
        if not password.isalnum() or len(password) == 0:
            return False
        return True
    
    @staticmethod
    def random_string():
        """
        Generate a random password
        :return: a random string
        :return:
        """
        str1 = ''.join((random.choice(string.ascii_letters) for x in range(6)))
        str1 += ''.join((random.choice(string.digits) for x in range(6)))

        sam_list = list(str1)
        random.shuffle(sam_list)
        final_string = ''.join(sam_list)
        return final_string
    
    @classmethod
    def area_name_of_acc(cls, user):
        if user.role == AccountType.admin:
            return "admin"
        elif user.role == AccountType.customer:
            return "customer"
        return ""
