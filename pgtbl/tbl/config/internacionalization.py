"""
Archive to take care of the internationalization of the project.
https://docs.djangoproject.com/en/1.11/topics/i18n/
"""

from django.utils.translation import ugettext_lazy as _

# Language selection
LANGUAGES = [
    ('pt-br', _('Portuguese')),
    ('en-us', _('English')),
    ('fr-ca', _('French'))
]

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
DEFAULT_LANGUAGE = 'pt-br'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
SAO_PAULO = 'America/Sao_Paulo'
USA = 'UTC'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
INTERNATIONALIZATION = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
FORMAT_DATES = True

# If you set this to False, Django will not use timezone-aware datetimes.
TIMEZONE_DATETIMES = True
