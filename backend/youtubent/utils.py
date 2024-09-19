import random
import string
from django.utils import timezone

def dumb_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=50))

def refresh_session(session):
    session.expire = timezone.now() + timezone.timedelta(days=7)
    session.save()