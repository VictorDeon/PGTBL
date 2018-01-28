from rolepermissions.permissions import register_object_checker
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@register_object_checker()
def crud_question_permission(permission, user, view):
    """
    Function to allows only teacher monitors to modify questions.
    """

    discipline = view.get_discipline()

    if user in discipline.monitors.all() or user == discipline.teacher:
        return True

    return False


@register_object_checker()
def show_questions_permission(permission, user, view):
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


@register_object_checker()
def irat_permissions(permission, user, view):
    """
    iRAT exam permissions.
    """

    session = view.get_session()

    irat_duration = timedelta(minutes=session.irat_duration)
    now = timezone.localtime(timezone.now())

    if now > session.irat_datetime and \
       (now - irat_duration) < session.irat_datetime:
           return True

    return False


@register_object_checker()
def grat_permissions(permission, user, view):
    """
    gRAT exam permissions.
    """

    session = view.get_session()

    grat_duration = timedelta(minutes=session.grat_duration)
    now = timezone.localtime(timezone.now())

    if now > session.grat_datetime and \
       (now - grat_duration) < session.grat_datetime:
           return True

    return False
