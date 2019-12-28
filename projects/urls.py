from django.urls import path

from projects.views import project_list, project_settings

app_name = 'projects'

urlpatterns = [
    path('', project_list.project_list, name='list'),
    path('details/<int:project_id>/settings/general', project_settings.general, name="project_settings_general"),
    path('details/<int:project_id>/settings/members', project_settings.members, name="project_settings_members"),
    path('details/<int:project_id>/settings/members/<int:member_id>', project_settings.members_edit,
         name="project_settings_members_edit"),
    path('details/<int:project_id>/settings/members/new', project_settings.members_new,
         name="project_settings_members_new")

]
