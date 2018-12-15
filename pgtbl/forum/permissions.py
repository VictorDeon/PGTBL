from rolepermissions.permissions import register_object_checker


@register_object_checker()
def show_forum(permission, user, view):
    """
    Only user inside discipline can see the forum
    """

    discipline = view.get_discipline()

    if (user in discipline.students.all() or
        user in discipline.monitors.all() or
        user == discipline.teacher):
        return True

    return False


@register_object_checker()
def edit_and_delete_topic_and_answer(permission, user, view):
    """
    Only the topic or answer owner can edit or delete it.
    """

    obj = view.get_object()

    if user == obj.author:
        return True

    return False


@register_object_checker()
def correct_answer(permission, user, view):
    """
    Only teacher or monitor or topic owner can approve a answer.
    """

    discipline = view.get_discipline()
    answer = view.get_object()

    if user == discipline.teacher or user in discipline.monitors.all() or user == answer.author:
        return True

    return False