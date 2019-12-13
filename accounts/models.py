from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.db import models

from accounts.managers import UserManager


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    email = models.EmailField(
        unique=True,
        db_index=True,
        max_length=255
    )

    first_name = models.CharField(
        max_length=255
    )

    last_name = models.CharField(
        max_length=255,
        blank=True
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name='Is user admin'
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Registration date of the user'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Is user active'
    )

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    def __str__(self):
        return self.email
