from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.permissions import PermissionMixin
from notification.models import Notification


class NotificationListView(LoginRequiredMixin,
                           PermissionMixin,
                           ListView):
    """
    View to see all notifications.
    """

    template_name = 'notification/list.html'
    paginate_by = 10
    context_object_name = 'notifications'

    permissions_required = []

    def get_queryset(self):
        """
        Get the discipline queryset from model database.
        """

        notifications = Notification.objects.filter(
            receiver=self.request.user
        )

        return notifications