"""
File to create decorator mixins
"""

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages


class UserCheckMixin(object):
    """
    Checks a user condition and if this condition is not
    satisfied redirects to a specific url
    """

    user_check_failure_path = ''

    def check_user(self, user):
        """
        If not override return always true.
        """

        return True

    def user_check_failed(self, request, *args, **kwargs):
        """
        If user check fail, redirect the user to another place.
        """

        return redirect(self.user_check_failure_path)

    def dispatch(self, request, *args, **kwargs):
        """
        Try to dispatch to the right method.
        """

        if not self.check_user(request.user):
            return self.user_check_failed(request, *args, **kwargs)

        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)


class PermissionRequiredMixin(UserCheckMixin):
    """
    Insert a permission in one class based view.
    """

    user_check_failure_path = reverse_lazy('accounts:login')
    permissions_required = None

    def check_user(self, user):
        """
        Verify if user has specific permission
        """

        if user.has_perms(self.permissions_required):
            return True

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        return False
