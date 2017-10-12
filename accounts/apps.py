from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = _('Accounts')
