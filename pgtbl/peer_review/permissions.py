from rolepermissions.permissions import register_object_checker


@register_object_checker()
def crud_peer_review(permission, user, view):
    """
    Update the Peer Review weight and available checkbox

    :param permission: Specific permission
    :param user: User authenticated
    :param view: View that run this permission
    :return: True if all conditions are met and false otherwise
    """

    discipline = view.get_discipline()

    if user == discipline.teacher:
        return True

    return False


@register_object_checker()
def show_peer_review_test(permission, user, view):
    """
    Permission that allows only students, monitors and teacher of specific
    discipline to see the peer review features and the peer review will be
    only available when the teacher do it.

    :param permission: Specific permission
    :param user: User authenticated
    :param view: View that run this permission
    :return: True if all conditions are met and false otherwise
    """

    discipline = view.get_discipline()
    session = view.get_session()

    if not session.peer_review_available and user != discipline.teacher:
        return False

    if user in discipline.students.all() or \
       user in discipline.monitors.all() or \
       user == discipline.teacher:
        return True

    return False


@register_object_checker()
def send_peer_review(permission, user, view):
    """
    Permission to only user in a specific group send a peer review.

    :param permission: Specific permission
    :param user: User authenticated
    :param view: View that run this permission
    :return: True if all conditions are met and false otherwise
    """

    discipline = view.get_discipline()
    session = view.get_session()
    group = view.get_student_group()
    student = view.get_student()

    if not group:
        return False

    if not session.peer_review_available:
        return False

    if student not in group.students.all():
        return False

    if user in discipline.students.all() and \
       user in group.students.all():
        return True

    return False