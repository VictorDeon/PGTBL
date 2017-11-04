"""
File to provides some global functionality for testing.
"""

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from disciplines.models import Discipline

# Get the custom user model
User = get_user_model()


def check_messages(self, response, tag, content):
    """
    Get the messages from django.contrib.messages
    Need to pass follow=True in the get or post method.
    """

    message = list(response.context.get('messages'))[0]
    self.assertEqual(message.tags, tag)
    self.assertEqual(message.message, _(content))


def list_transform(queryset):
    """
    Transform the queryset in a list to compare.
    """

    query_list = []

    for item in queryset:
        query_list.append(item)

    return query_list


def user_factory(qtd=1,
                 username='Test',
                 email='test',
                 password='test1234',
                 is_teacher=True,
                 count=0,
                 **fields):
    """
    Create N users and return a list.
    """

    users = []

    for n in range(qtd):
        user = User.objects.create_user(
            username='{0}{1}'.format(username, n+count),
            email='{0}{1}@gmail.com'.format(email, n+count),
            password=password,
            is_teacher=is_teacher,
            **fields
        )

        users.append(user)

    if qtd > 1:
        return users
    else:
        return user
