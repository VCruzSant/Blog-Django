import string
from random import SystemRandom
from django.utils.text import slugify


def random_letters(k=5):
    return ''.join(SystemRandom().choices(
        string.ascii_lowercase + string.digits, k=k
    ))


def slugify_new(txt, k=5):
    return slugify(txt) + '-' + random_letters(k)
