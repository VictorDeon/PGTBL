from rolepermissions.permissions import register_object_checker


@register_object_checker()
def change_own_discipline(role, user, discipline):
    """
    Function to verify if user is the discipline owner.
    Admin user can change all disciplines
    """

    if user.id == discipline.teacher.id:
        return True

    return False
