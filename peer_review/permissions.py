from rolepermissions.permissions import register_object_checker
from django.contrib.auth import get_user_model

User = get_user_model()

@register_object_checker()
def only_student_can_change(permission, user, view):
    """
    Only the discipline students can change the students grades
    """

    discipline = view.get_discipline()

    if user in discipline.students.all():
        return True

    return False
