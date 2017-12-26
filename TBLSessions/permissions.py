from rolepermissions.permissions import register_object_checker
from django.contrib.auth import get_user_model

User = get_user_model()


@register_object_checker()
def change_own_session(permission, user, view):
    """
    Function to verify if user is the discipline owner.
    Admin user can change all sessions
    """

    # Verify if view has the method get_discipline
    if bool(getattr(view, 'get_discipline', None)):
        discipline = view.get_discipline()
    else:
        discipline = view.get_object()

    if user == discipline.teacher:
        return True

    return False


@register_object_checker()
def show_sessions_permission(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see discipline session features.
    """

    discipline = view.get_discipline()

    if user in discipline.students.all() or \
       user in discipline.monitors.all() or \
       user == discipline.teacher:
        return True

    return False
