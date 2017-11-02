from rolepermissions.roles import AbstractUserRole


class Teacher(AbstractUserRole):
    """
    Group that contain teacher permissions.
    """

    available_permissions = {
        'create_discipline': True,
    }


class Student(AbstractUserRole):
    """
    Group that contain student permissions.
    """

    available_permissions = {}


class Monitor(AbstractUserRole):
    """
    Group that contain monitor permissions.
    """

    available_permissions = {}
