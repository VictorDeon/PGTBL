from rolepermissions.permissions import register_object_checker
from django.contrib.auth import get_user_model

User = get_user_model()

@register_object_checker()
def show_rank_permission(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see discipline rank features.
    """

    discipline = view.get_discipline()

    if not discipline.was_group_provided and user != discipline.teacher:
        return False

    if user in discipline.students.all() or \
       user in discipline.monitors.all() or \
       user == discipline.teacher:
        return True

    return False

@register_object_checker()
def show_hall_of_fame(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see discipline hall of fame.
    """

    discipline = view.get_discipline()

    if user in discipline.students.all() or \
       user in discipline.monitors.all() or \
       user == discipline.teacher:
        return True

    return False