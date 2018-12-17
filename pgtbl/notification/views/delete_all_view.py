from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages

from core.permissions import PermissionMixin
from notification.models import Notification


class NotificationDeleteAllView(LoginRequiredMixin,
                                PermissionMixin,
                                DeleteView):
    """
    View to delete all user notification.
    """

    model = Notification

    # Permissions
    permissions_required = []

    def get_queryset(self):
        """
        Get all notification to be deleted
        """

        notifications = Notification.objects.filter(
            receiver=self.request.user
        )

        return notifications

    def delete(self, request, *args, **kwargs):
        """
        Delete all notifications
        """

        notifications = self.get_queryset()

        notifications.delete()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy('notifications:list')

        messages.success(self.request, _("Notifications clean successfully."))

        return success_url