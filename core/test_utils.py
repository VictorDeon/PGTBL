"""
File to provides some global functionality for testing.
"""

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from core.utils import insert_group_permissions

# Get the custom user model
User = get_user_model()


def create_user(username, email, password='test1234', is_teacher=False):
    """
    Create a teacher with his permissions.
    """

    user = User(
        username=username,
        email=email,
        is_teacher=is_teacher
    )

    user.set_password(password)
    user.save()

    teacher_permissions = [
        'add_discipline',
        'change_discipline',
        'delete_discipline'
    ]

    student_permissions = []

    if user.is_teacher is True:
        group = user.groups.get(name='Teacher')
        insert_group_permissions(group, teacher_permissions)
    else:
        group = user.groups.get(name='Student')
        insert_group_permissions(group, student_permissions)

    return user


def check_messages(self, response, tag, content):
    """
    Get the messages from django.contrib.messages
    Need to pass follow=True in the get or post method.
    """

    message = list(response.context.get('messages'))[0]
    self.assertEqual(message.tags, tag)
    self.assertEqual(message.message, _(content))
