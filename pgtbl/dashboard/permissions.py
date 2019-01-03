from rolepermissions.permissions import register_object_checker


@register_object_checker()
def show_dashboard_permission(permission, user, view):
    """
    Only students can access the gamification dashboard.
    """

    discipline = view.get_discipline()
    session = view.get_session()

    if user in discipline.students.all() and not session.is_closed:
        return True

    return False


@register_object_checker()
def show_report_permission(permission, user, view):
    """
    Only teacher can access the report.
    """

    discipline = view.get_discipline()

    if user == discipline.teacher:
        return True

    return False