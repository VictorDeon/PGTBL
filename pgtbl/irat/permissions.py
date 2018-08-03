from rolepermissions.permissions import register_object_checker
from django.utils import timezone
from datetime import timedelta

@register_object_checker()
def crud_tests(permission, user, view):
    """
    Create and Update irat and grat tests.
    """

    discipline = view.get_discipline()

    if user == discipline.teacher:
        return True

    return False

@register_object_checker()
def show_questions_permission(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see the exercises list session features.
    """

    discipline = view.get_discipline()
    session = view.get_session()

    if user in discipline.students.all() and not session.is_closed:
        return True

    if user in discipline.monitors.all() or \
       user == discipline.teacher:
        return True

    return False

@register_object_checker()
def show_test_result(permission, user, view):
    """
    Student only can see the result after the gRAT is finished.
    """

    session = view.get_session()
    discipline = view.get_discipline()

    grat_duration = timedelta(minutes=session.grat_duration)
    now = timezone.localtime(timezone.now())

    if user == discipline.teacher:
        return True

    # If grat date and time is null only the teacher can change
    if not session.grat_datetime:
        return False

    if now > (session.grat_datetime + grat_duration):
        return True

    return False


@register_object_checker()
def irat_permissions(permission, user, view):
    """
    iRAT exam permissions.
    """

    session = view.get_session()
    discipline = view.get_discipline()

    irat_duration = timedelta(minutes=session.irat_duration)
    now = timezone.localtime(timezone.now())

    if user == discipline.teacher:
        return True

    # If irat date and time is null only the teacher can change
    if not session.irat_datetime:
        return False

    if now > session.irat_datetime and \
       (now - irat_duration) < session.irat_datetime:
           return True

    return False