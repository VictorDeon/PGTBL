from rolepermissions.permissions import register_object_checker
from django.contrib.auth import get_user_model

User = get_user_model()


@register_object_checker()
def monitor_can_change(permission, user, view):
    """
    Function to allows all monitors to modify something.
    """

    discipline = view.get_discipline()

    if user in discipline.monitors.all() or user == discipline.teacher:
        return True

    return False


@register_object_checker()
def show_files_permission(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see discipline files features.
    """

    discipline = view.get_discipline()

    if user in discipline.students.all() or \
       user in discipline.monitors.all() or \
       user == discipline.teacher:
        return True

    return False


@register_object_checker()
def show_tbl_file_session(permission, user, view):
    """
    Permission that allows only enter in tbl session files if its available.
    """

    discipline = view.get_discipline()
    session = view.get_session()

    if session.is_closed and \
       user not in discipline.monitors.all() and \
       user != discipline.teacher:
        return False

    return True
