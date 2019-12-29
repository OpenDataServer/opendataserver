from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from accounts.models import User
from projects.forms.project_settings import MemberNewSettingsForm, GeneralSettingsForm, MemberEditSettingsForm
from projects.models import Project, ProjectMember


def general(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.has_project_permission(project, "admin"):
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
    else:
        raise PermissionDenied


def members(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.has_project_permission(project=project, minimum_needed_permission="admin"):
        project_members = ProjectMember.objects.filter(
            project=project
        )
        return render(
            request=request,
            template_name='details/settings/members.html',
            context={
                'members': project_members,
                'current_user': request.user
            }
        )
    else:
        raise PermissionDenied


def members_edit(request, project_id, member_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.has_project_permission(project=project, minimum_needed_permission="admin"):
        project_member = get_object_or_404(
            ProjectMember,
            id=member_id,
            project=project
        )
        if request.method == 'POST':
            form = MemberEditSettingsForm(request.POST)
            if form.is_valid():
                project_member.role = form.cleaned_data['role']
                project_member.save()
                return redirect('projects:project_settings_members', project_id=project_id)
            return render(
                request=request,
                template_name='details/settings/members_new.html',
                context={
                    'form': form
                }
            )
        else:
            form = MemberEditSettingsForm(
                initial={
                    "role": project_member.role
                })
            return render(
                request=request,
                template_name='details/settings/members_edit.html',
                context={
                    'form': form,
                    'project_member': project_member
                }
            )
    else:
        raise PermissionDenied


def members_new(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user.has_project_permission(project=project, minimum_needed_permission="admin"):
        if request.method == 'POST':
            form = MemberNewSettingsForm(request.POST)
            if form.is_valid():
                user = User.objects.get(email=form.cleaned_data['email'])
                project = Project.objects.get(id=project_id)
                if ProjectMember.objects.filter(user=user, project=project).count() == 0:
                    ProjectMember.objects.create(user=user, role=form.cleaned_data['role'], project=project)
                    return redirect('projects:project_settings_members', project_id=project_id)
                else:
                    form.add_error("email", "The user is already member in the project")
            return render(
                request=request,
                template_name='details/settings/members_new.html',
                context={
                    'form': form
                }
            )
        else:
            form = MemberNewSettingsForm()
            return render(
                request=request,
                template_name='details/settings/members_new.html',
                context={
                    'form': form
                }
            )
    else:
        raise PermissionDenied
