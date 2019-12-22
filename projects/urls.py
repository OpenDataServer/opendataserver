from django.urls import path

from projects.views import project_list

app_name = 'projects'

urlpatterns = [
    path('', project_list.project_list, name='list'),
]