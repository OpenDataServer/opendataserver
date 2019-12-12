from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str = None, **kwargs):
        if not email:
            raise ValueError(_('The Email must be set'))
        user = self.model(
            email=email,
            **kwargs
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, given_name: str, password: str = None):
        user = self.model(
            email=email,
            given_name=given_name,
        )
        user.set_password(password)
        user.is_staff = True
        user.save()
        return user
