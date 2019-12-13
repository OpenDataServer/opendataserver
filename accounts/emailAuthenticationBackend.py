from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class EmailAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            return None
