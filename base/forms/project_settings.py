from django import forms
from django.utils.translation import gettext_lazy

from base.models import Project, ProjectMember


class GeneralSettingsForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)


class MemberEditSettingsForm(forms.ModelForm):
    class Meta:
        model = ProjectMember
        fields = ('role',)

    role = forms.ChoiceField(
        choices=[
            ("admin", gettext_lazy("Admin")),
            ("member", gettext_lazy("Member")),
            ("restricted", gettext_lazy("Restricted"))

        ],
        label=gettext_lazy("Role"),
    )


class MemberNewSettingsForm(forms.Form):
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
        required=True
    )
