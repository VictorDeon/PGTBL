from rolepermissions.permissions import register_object_checker


@register_object_checker()
def show_session_grades(permission, user, view):
    """
    Permission that allows only enter in tbl session if its available.
    """

    discipline = view.get_discipline()
    session = view.get_session()

    if session.is_closed and \
       user not in discipline.monitors.all() and \
       user != discipline.teacher:
        return False

    return True


@register_object_checker()
def only_teacher_can_change(permission, user, view):
    """
    Only the discipline teacher can change the student grades
    """

    discipline = view.get_discipline()

    if user == discipline.teacher:
        return True

    return False
