from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email: str, first_name: str, password: str, last_name: str = ""):
        if not email:
            raise ValueError('The Email must be set')
        if not first_name:
            raise ValueError('The first name must be set')
        if not password:
            raise ValueError('The password must be set')
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, first_name: str, password: str, last_name: str = ""):
        if not email:
            raise ValueError('The Email must be set')
        if not first_name:
            raise ValueError('The first name must be set')
        if not password:
            raise ValueError('The password must be set')
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user
