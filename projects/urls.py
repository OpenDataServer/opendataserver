from django.urls import path

from projects.views import project_list, project_settings

app_name = 'projects'

urlpatterns = [
    path('', project_list.project_list, name='list'),
    path('details/<int:project_id>/settings/general', project_settings.general, name="project_settings_general")
]
