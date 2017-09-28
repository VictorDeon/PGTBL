import os
import django
from django.conf import settings

# We manually designate which settings we will be using in an environment
# variable. This is similar to what occurs in the `manage.py`
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tbl.settings')


def pytest_configure():
    """
    pytest automatically calls this function once when tests are running.
    """

    settings.DEBUG = False
    django.setup()
