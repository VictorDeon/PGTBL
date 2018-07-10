from rolepermissions.permissions import register_object_checker
from django.contrib.auth import get_user_model

User = get_user_model()


@register_object_checker()
def show_ranking_permission(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see rankingGroup details features.
    """

    discipline = view.get_object() 

    if user in discipline.students.all() or \
       user in discipline.monitors.all() or \
       user == discipline.teacher:
        return True

    return False
