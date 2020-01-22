from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.urls import get_script_prefix, resolve
from django.utils.translation import get_language, gettext

from base.models import Project


class EventMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith(get_script_prefix() + get_language() + '/project') and not request.path.startswith(get_script_prefix() + get_language() + '/projects'):
            return self.get_response(request)

        url = resolve(request.path_info)
        if 'project_id' in url.kwargs:
            try:
                request.project = Project.objects.get(id=url.kwargs['project_id'])
            except ObjectDoesNotExist:
                raise Http404(gettext("The selected project was not found"))
        return self.get_response(request)
