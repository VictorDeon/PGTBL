from rolepermissions.permissions import register_object_checker
from django.utils import timezone
from datetime import timedelta

@register_object_checker()
def crud_question_permission(permission, user, view):
    """
    Function to allows only teacher monitors to modify questions.
    """

    discipline = view.get_discipline()

    if user in discipline.monitors.all() or user == discipline.teacher:
        return True

    return False