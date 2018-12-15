from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages

from core.permissions import PermissionMixin
from notification.models import Notification


class NotificationDeleteView(LoginRequiredMixin,
                             PermissionMixin,
                             DeleteView):
    """
    View to delete a specific user notification.
    """

    model = Notification

    # Permissions
    permissions_required = []

    def get_object(self, queryset=None):
        """
        Get the notification to be deleted
        """

        notification = get_object_or_404(
            Notification,
            pk=self.kwargs.get('pk', '')
        )

        return notification

    def get_success_url(self):
        """
        Get success url to redirect.
        """

        success_url = reverse_lazy('notifications:list')

        messages.success(self.request, _("Notification deleted successfully."))

        return success_url
