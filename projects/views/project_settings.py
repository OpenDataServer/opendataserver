from django import forms
from django.shortcuts import render, get_object_or_404, redirect

from projects.models import Project


class GeneralSettingsForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name',)


def general(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = GeneralSettingsForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return render(
                request=request,
                template_name='details/settings/general.html',
                context={'form': form}
            )

    else:
        form = GeneralSettingsForm(instance=project)
        return render(
            request=request,
            template_name='details/settings/general.html',
            context={'form': form}
        )
