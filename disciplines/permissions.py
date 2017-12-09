from rolepermissions.permissions import register_object_checker
from django.contrib.auth import get_user_model

User = get_user_model()


@register_object_checker()
def change_own_discipline(permission, user, view):
    """
    Function to verify if user is the discipline owner.
    Admin user can change all disciplines
    """

    discipline = view.get_object()

    if user == discipline.teacher:
        return True

    return False


@register_object_checker()
def show_discipline_permission(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see discipline details features.
    """

    discipline = view.get_object()

    if user in discipline.students.all() or \
       user in discipline.monitors.all() or \
       user == discipline.teacher:
        return True

    return False


@register_object_checker()
def show_discipline_students_permission(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see discipline list features.
    """

    discipline = view.get_discipline()

    students = discipline.students.all()
    monitors = discipline.monitors.all()

    if user in students or \
       user in monitors or \
       user == discipline.teacher:
        return True

    return False


@register_object_checker()
def show_users_to_insert_in_discipline_permission(permission, user, view):
    """
    Permission that allows only teacher of specific discipline to see
    users to insert inside discipline.
    """

    discipline = view.get_discipline()

    if user == discipline.teacher:
        return True

    return False
