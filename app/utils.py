import string
import random
import re

URL_REGEX = re.compile(
    r'^(https?://)?'        
    r'([\da-z.-]+)\.([a-z.]{2,6})'
    r'([/\w .-]*)*/?$' 
)
ID_LENGTH = 7


def generate_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=ID_LENGTH))


def is_url_valid(url):
    return bool(URL_REGEX.match(url))
