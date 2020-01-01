from django.urls import path

from base.views import projects
from base.views.project import settings

app_name = 'base'

urlpatterns = [
    path('projects/', projects.projects_list, name='projects_list'),
    path('projects/new/', projects.projects_new, name='projects_new'),
    path('project/<int:project_id>/settings/general', settings.general, name="project_settings_general"),
    path('project/<int:project_id>/settings/members', settings.members, name="project_settings_members"),
    path('project/<int:project_id>/settings/members/<int:member_id>', settings.members_edit,
         name="project_settings_members_edit"),
    path('project/<int:project_id>/settings/members/new', settings.members_new,
         name="project_settings_members_new")

]
