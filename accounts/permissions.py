from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext


def project_permission_required(minimum_needed_permission):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # just a double check
                raise PermissionDenied()
            if request.user.has_project_permission(
                project=request.project,
                minimum_needed_permission=minimum_needed_permission
            ):
                return function(request, *args, **kwargs)
            raise PermissionDenied(gettext("You do not have the permission to view this project"))
        return wrapper
    return decorator


class ProjectPermissionRequiredMixin:
    permission = ''

    @classmethod
    def as_view(cls, **kwargs):
        view = super(ProjectPermissionRequiredMixin, cls).as_view(**kwargs)
        return project_permission_required(cls.permission)(view)
