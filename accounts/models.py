from django.contrib.auth.models import AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from accounts.managers import UserManager
from projects.models import ProjectMember


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

    def has_project_permission(self, project_id, minimum_needed_permission="owner", project=None) -> bool:
        if project:
            try:
                project_member = ProjectMember.objects.get(user=self, project=project)
            except ObjectDoesNotExist:
                return False
        else:
            try:
                project_member = ProjectMember.objects.get(user=self, project_id=project_id)
            except ObjectDoesNotExist:
                return False

        if minimum_needed_permission == "owner" and project_member.role == "owner":
            return True
        elif minimum_needed_permission == "admin" and (project_member.role == "owner" or project_member.role == "admin"):
            return True
        elif minimum_needed_permission == "member" and (project_member.role == "owner" or project_member.role == "admin" or project_member.role == "member"):
            return True
        elif minimum_needed_permission == "restricted":
            return True
        else:
            return False

    def __str__(self):
        return self.email
