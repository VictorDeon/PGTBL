"""
File that inserts global contexts in all django templates.
Just insert this file into the template processors in the settings.
"""

from django.utils import timezone


def today_date(request):
    """
    Insert today date inside templates.
    """

    context = {
        'date': timezone.localtime(timezone.now())
    }

    return context
