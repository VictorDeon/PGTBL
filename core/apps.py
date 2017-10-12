from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = _('News')
