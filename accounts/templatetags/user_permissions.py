from django import template

register = template.Library()


@register.simple_tag
def has_user_project_permission(user, minimum_needed_permission, project_id=None, project=None):
    if project:
        return user.has_project_permission(project=project, minimum_needed_permission=minimum_needed_permission)
    else:
        return user.has_project_permission(project_id=project_id, minimum_needed_permission=minimum_needed_permission)
