"""
File to provides some global functionality for testing.
"""

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

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
