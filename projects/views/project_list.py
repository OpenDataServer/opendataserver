from django.shortcuts import render

from projects.models import ProjectMember, ProjectDevice


def project_list(request):
    project_participants = ProjectMember.objects.filter(user=request.user)
    projects = []
    for project_participant in project_participants:
        project = project_participant.project
        projects.append({
            "name": project.name,
            "devices_count": ProjectDevice.objects.filter(project=project).count(),
            "members_count": ProjectMember.objects.filter(project=project).count(),
            "user_role": project_participant.get_role_display()
        })
    return render(
        request=request,
        template_name='list.html',
        context={'projects': projects}
    )
