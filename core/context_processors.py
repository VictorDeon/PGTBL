"""
File that inserts global contexts in all django templates.
Just insert this file into the template processors in the settings.
"""

from datetime import datetime


def today_date(request):
    context = {
        'date': datetime.now()
    }

    return context
