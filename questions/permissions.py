from rolepermissions.permissions import register_object_checker
from django.contrib.auth import get_user_model

User = get_user_model()


@register_object_checker()
def crud_exercise_permission(permission, user, view):
    """
    Function to allows only teacher monitors to modify questions.
    """

    discipline = view.get_discipline()

    if user in discipline.monitors.all() or user == discipline.teacher:
        return True

    return False


@register_object_checker()
def show_exercise_permission(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see the exercise list session features.
    """

    discipline = view.get_discipline()

    if user in discipline.students.all() or \
       user in discipline.monitors.all() or \
       user == discipline.teacher:
        return True

    return False
