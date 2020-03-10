from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
from django.utils.translation import gettext_lazy

from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class GeneralUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class EmailChangeForm(forms.Form):
    email = forms.CharField(
        max_length=255,
        required=True,
        label=gettext_lazy("New e-mail address"),
    )
    email_repeat = forms.CharField(
        max_length=255,
        required=True,
        label=gettext_lazy("New e-mail address (repeat)")
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(gettext_lazy("There is already an account with this e-mail address"))
        return email

    def clean_email_repeat(self):
        email = self.cleaned_data.get('email')
        email_repeat = self.cleaned_data.get('email_repeat')
        if email != email_repeat:
            raise forms.ValidationError(gettext_lazy("The e-mail address does not equal the repeated e-mail address"))
        return email_repeat


class PasswordChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ()

    old_password = forms.CharField(
        max_length=255,
        required=True,
        label=gettext_lazy("Current password"),
        widget=forms.PasswordInput()
    )
    new_password = forms.CharField(
        max_length=255,
        required=True,
        label=gettext_lazy("New password"),
        widget=forms.PasswordInput()
    )
    new_password_repeat = forms.CharField(
        max_length=255,
        required=True,
        label=gettext_lazy("New password (repeat)"),
        widget=forms.PasswordInput()
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if old_password and not check_password(old_password, self.instance.password):
            raise forms.ValidationError(gettext_lazy("Please enter your current password"))
        return old_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password and validate_password(new_password, user=self.instance) is not None:
            raise forms.ValidationError(gettext_lazy(password_validators_help_texts()))
        return new_password

    def clean_new_password_2(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_repeat = self.cleaned_data.get('new_password_repeat')
        if new_password and new_password != new_password_repeat:
            raise forms.ValidationError("Please enter the same password twice")

    def clean(self):
        if self.cleaned_data.get('new_password'):
            self.instance.set_password(self.cleaned_data.get('new_password'))
        return self.cleaned_data
