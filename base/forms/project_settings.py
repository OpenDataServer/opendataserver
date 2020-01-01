from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy

from accounts.models import User
from base.models import Project


class GeneralSettingsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)


class MemberEditSettingsForm(forms.Form):
    role = forms.ChoiceField(
        choices=[
            ("admin", gettext_lazy("Admin")),
            ("member", gettext_lazy("Member")),
            ("restricted", gettext_lazy("Restricted"))

        ],
        label=gettext_lazy("Role"),
    )


class MemberNewSettingsForm(forms.Form):
    def user_exists(self):
        try:
            User.objects.get(email=self)
        except ObjectDoesNotExist:
            raise forms.ValidationError("There is no user with the e-mail address")

    role = forms.ChoiceField(
        choices=[
            ("admin", gettext_lazy("Admin")),
            ("member", gettext_lazy("Member")),
            ("restricted", gettext_lazy("Restricted"))

        ],
        label=gettext_lazy("Role"),
        required=True
    )
    email = forms.CharField(
        max_length=255,
        label=gettext_lazy("E-Mail address of the user"),
        required=True,
        validators=[user_exists, ]
    )
