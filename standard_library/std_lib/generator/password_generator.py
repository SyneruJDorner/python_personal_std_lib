import random
import string

def password_generator(password_length=8, lower_case=True, upper_case=True, numbers=True, symbols=True):
    '''
    Generates a random password of the specified length.

    Parameters:
    -----------
    password_length: int
        The length of the password to be generated (default: 8)
    upper_case: bool
        Whether or not to include upper case letters (default: True)
    lower_case: bool
        Whether or not to include lower case letters (default: True)
    numbers: bool
        Whether or not to include numbers (default: True)
    symbols: bool
        Whether or not to include symbols (default: True)
    '''
    all = ""
    all += string.ascii_lowercase  if lower_case else ""
    all += string.ascii_uppercase  if upper_case else ""
    all += string.digits  if numbers else ""
    all += string.punctuation if symbols else ""

    temp = random.sample(all, password_length)
    random_password = ''.join(temp)
    return random_password
