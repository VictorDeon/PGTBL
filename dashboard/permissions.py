from rolepermissions.permissions import register_object_checker
from django.contrib.auth import get_user_model

User = get_user_model()

@register_object_checker()
def only_teacher_can_change(permission, user, view):
    """
    Only the discipline teacher can see the dashboard
    """

    discipline = view.get_discipline()

    if user == discipline.teacher:
        return True

    return False
