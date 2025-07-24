import string
import random
import re

__all__ = ['generate_id', 'is_url_valid']

ID_LENGTH = 7
URL_REGEX = re.compile(
    r'^(https?://)?'        
    r'([\da-z.-]+)\.([a-z.]{2,6})'
    r'([/\w .-]*)*/?$' 
)

def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=ID_LENGTH))


def is_url_valid(url):
    return bool(URL_REGEX.match(url))
