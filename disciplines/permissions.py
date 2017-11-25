from rolepermissions.permissions import register_object_checker
from disciplines.models import Discipline
from django.contrib.auth import get_user_model

User = get_user_model()


@register_object_checker()
def change_own_discipline(permission, user, view):
    """
    Function to verify if user is the discipline owner.
    Admin user can change all disciplines
    """

    discipline = view.get_object()

    if user.id == discipline.teacher.id:
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
       user.id == discipline.teacher.id:
        return True

    return False


@register_object_checker()
def show_discipline_students_permission(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see discipline list features.
    """

    students = view.get_queryset()
    discipline = view.discipline

    if user in students or user.id == discipline.teacher.id:
        return True

    return False
