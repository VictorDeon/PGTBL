# Python functions
import hashlib
import string
import random


# --------------------------- RESET PASSWORD KEY -------------------------- #


def random_key(size=5):
    """
    Generates the key with a random character set.
    """

    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(size))


def generate_hash_key(salt, random_str_size=5):
    """
    Function to generate the hash key from the salt which is some user
    information.
    """

    random_str = random_key(random_str_size)
    text = random_str + salt
    return hashlib.sha224(text.encode('utf-8')).hexdigest()
