from django import forms
from django.utils.translation import gettext_lazy


class ProjectNewForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label=gettext_lazy("Project name"),
        required=True
    )
