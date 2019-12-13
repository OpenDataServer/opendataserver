from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm

from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_staff')

    def clean_password(self):
        return self.initial["password"]
