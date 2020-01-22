from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.utils.translation import gettext
from django.views.generic import UpdateView, TemplateView

from accounts.models import User
from accounts.permissions import ProjectPermissionRequiredMixin
from base.forms.project_settings import MemberNewSettingsForm, GeneralSettingsForm, MemberEditSettingsForm
from base.models import Project, ProjectMember


# Check Permissions


class GeneralSettingsView(ProjectPermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission = "admin"
    template_name = "project/settings/general.html"
    form_class = GeneralSettingsForm
    success_message = gettext("Your changes have been saved.")

    def get_success_url(self):
        return reverse_lazy("base:project_settings_general", args=[self.kwargs['project_id']])

    def get_object(self, queryset=None):
        project = Project.objects.get(id=self.kwargs['project_id'])
        return project


class MemberSettingsView(ProjectPermissionRequiredMixin, TemplateView):
    permission = "admin"
    template_name = "project/settings/members.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_members = ProjectMember.objects.filter(
            project=self.request.project
        )
        context['members'] = project_members
        return context


class MemberEditSettingsView(ProjectPermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission = "admin"
    template_name = "project/settings/members_edit.html"
    form_class = MemberEditSettingsForm
    success_message = gettext("Your changes have been saved.")

    def get_success_url(self):
        return reverse_lazy("base:project_settings_members", args=[self.kwargs['project_id']])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_member'] = self.object
        return context

    def get_object(self, queryset=None):
        project_member = get_object_or_404(
            ProjectMember,
            id=self.kwargs['member_id'],
            project=self.request.project
        )
        return project_member


class MemberNewSettingsView(ProjectPermissionRequiredMixin, TemplateView):
    permission = "admin"
    template_name = "project/settings/members_new.html"

    @cached_property
    def add_form(self):
        return MemberNewSettingsForm(data=(self.request.POST if self.request.method == "POST" else None))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = self.add_form
        return ctx

    def post(self, request, *args, **kwargs):
        if self.add_form.is_valid():
            try:
                user = User.objects.get(email__iexact=self.add_form.cleaned_data['email'])
            except User.DoesNotExist:
                messages.error(self.request, gettext("Users need to have an account before they can be invited."))
                return self.get(request, *args, **kwargs)

            if ProjectMember.objects.filter(user=user, project_id=kwargs['project_id']).count() != 0:
                messages.error(self.request, gettext("The user is already member in the project."))
                return self.get(request, *args, **kwargs)

            else:
                ProjectMember.objects.create(
                    user=user,
                    role=self.add_form.cleaned_data['role'],
                    project_id=kwargs['project_id']
                )
                messages.success(self.request, gettext("The new member has been added to the project."))
                return redirect('base:project_settings_members', project_id=kwargs['project_id'])
