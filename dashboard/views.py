# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import (ListView)

# Application imports
from core.permissions import PermissionMixin

# Get the custom user from settings
User = get_user_model()


class DashboardView(LoginRequiredMixin,
                    PermissionMixin,
                    ListView):
    """
    Show the Dashboard page.
    """

    template_name = 'dashboard/list.html'
    permissions_required = [
        'only_teacher_can_change'
    ]


