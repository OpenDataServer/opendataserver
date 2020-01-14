from django.shortcuts import render, redirect

from base.forms.projects import ProjectNewForm
from base.models import ProjectMember, ProjectDevice, Project
from base.tasks import project_add_continuous_query


def projects_list(request):
    project_members = ProjectMember.objects.filter(user=request.user)
    projects = []
    for project_member in project_members:
        project = project_member.project
        projects.append({
            "name": project.name,
            "devices_count": ProjectDevice.objects.filter(project=project).count(),
            "members_count": ProjectMember.objects.filter(project=project).count(),
            "user_role": project_member.get_role_display()
        })
    return render(
        request=request,
        template_name='projects/list.html',
        context={'projects': projects}
    )


def projects_new(request):
    if request.method == 'POST':
        form = ProjectNewForm(request.POST)
        if form.is_valid():
            project = Project.objects.create(name=form.cleaned_data['name'])
            ProjectMember.objects.create(project=project, role="owner", user=request.user)
            project_add_continuous_query.apply_async(args=(project.id,))
            return redirect("base:projects_list")
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
