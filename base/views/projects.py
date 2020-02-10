from django.shortcuts import render, redirect

from base.forms.projects import ProjectNewForm
from base.models import ProjectMember, Project
from base.tasks import project_add_continuous_query


def projects_new(request):
    if request.method == 'POST':
        form = ProjectNewForm(request.POST)
        if form.is_valid():
            project = Project.objects.create(name=form.cleaned_data['name'])
            ProjectMember.objects.create(project=project, role="owner", user=request.user)
            project_add_continuous_query.apply_async(args=(project.pk,))
            return redirect("base:project_devices_list", project_id=project.pk)
        return render(
            request=request,
            template_name='projects/new.html',
            context={
                'form': form
            }
        )
    else:
        form = ProjectNewForm()
        return render(
            request=request,
            template_name='projects/new.html',
            context={
                'form': form
            }
        )
