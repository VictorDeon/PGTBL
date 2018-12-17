from rolepermissions.permissions import register_object_checker


@register_object_checker()
def show_appeals(permission, user, view):
    """
    Only user inside discipline can see the appeals and the session
    need to be open
    """

    discipline = view.get_discipline()
    session = view.get_session()

    if user == discipline.teacher:
        return True

    if (user in discipline.students.all() or
        user in discipline.monitors.all() and
        not session.is_closed):
        return True

    return False


@register_object_checker()
def create_appeal(permission, user, view):
    """
    Only students can create a appeal.
    """

    discipline = view.get_discipline()
    session = view.get_session()

    if user in discipline.students.all() and not session.is_closed:
        return True

    return False


@register_object_checker()
def edit_and_delete_appeal(permission, user, view):
    """
    Only the appeal owner can edit or delete a appeal.
    """

    appeal = view.get_object()

    if user == appeal.student:
        return True

    return False


@register_object_checker()
def delete_comment_appeal(permission, user, view):
    """
    Only the comment owner can delete a comment.
    """

    comment = view.get_object()

    if user == comment.author:
        return True

    return False


@register_object_checker()
def approve_appeal(permission, user, view):
    """
    Only teacher can approve a appeal.
    """

    discipline = view.get_discipline()

    if user == discipline.teacher:
        return True

    return False