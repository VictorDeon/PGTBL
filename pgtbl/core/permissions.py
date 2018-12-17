"""
File to create decorator mixins
"""

from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages

# Permission app
from rolepermissions.checkers import (
    has_permission,
    has_object_permission
)


class ModelPermissionMixin(object):
    """
    Insert a model permission in one class based view.
    """

    failure_redirect_path = reverse_lazy('accounts:login')

    permissions_required = None

    def check_permission(self, user):
        """
        Verify if user has specific group permission
        """

        for permission in self.permissions_required:
            if not has_permission(user, permission):
                return False

        return True

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        return self.failure_redirect_path

    def check_failed(self, request, *args, **kwargs):
        """
        If user check fail, redirect the user to another place.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        return redirect(self.get_failure_redirect_path())

    def dispatch(self, request, *args, **kwargs):
        """
        Try to dispatch to the right method.
        """

        if not self.check_permission(request.user):
            return self.check_failed(request, *args, **kwargs)

        return super(ModelPermissionMixin, self).dispatch(
            request, *args, **kwargs
        )


class PermissionMixin(object):
    """
    Insert a permission in one class based view.
    """

    failure_redirect_path = reverse_lazy('accounts:profile')

    permissions_required = None

    def check_permission(self, user, view):
        """
        Verify if user has permission.
        """

        for permission in self.permissions_required:
            if not has_object_permission(permission, user, view):
                return False

        return True

    def get_failure_redirect_path(self):
        """
        Get the failure redirect path.
        """

        messages.error(
            self.request,
            _("You are not authorized to do this action.")
        )

        return self.failure_redirect_path

    def check_failed(self, request, *args, **kwargs):
        """
        If user check fail, redirect the user to another place.
        """

        return redirect(self.get_failure_redirect_path())

    def dispatch(self, request, *args, **kwargs):
        """
        Try to dispatch to the right method.
        """

        if not self.check_permission(request.user, self):
            return self.check_failed(request, *args, **kwargs)

        return super(PermissionMixin, self).dispatch(
            request, *args, **kwargs
        )
