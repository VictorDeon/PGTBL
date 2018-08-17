from rolepermissions.permissions import register_object_checker


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
