from rolepermissions.permissions import register_object_checker
from django.contrib.auth import get_user_model

User = get_user_model()

@register_object_checker()
def only_student_can_change(permission, user, view):
    """
    Only the discipline students can make a peer review
    """

    discipline = view.get_discipline()

    if user in discipline.students.all():
        return True

    return False

@register_object_checker()
def only_teacher_can_change(permission, user, view):
    """
    Only the discipline teacher can see the peer review results
    """

    discipline = view.get_discipline()

    if user == discipline.teacher:
        return True

    return False
