from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.permissions import PermissionMixin
from disciplines.models import Discipline


class DisciplineDetailView(LoginRequiredMixin,
                           PermissionMixin,
                           DetailView):
    """
    View to show a specific discipline.
    """

    model = Discipline
    template_name = 'disciplines/details.html'
    permissions_required = [
        'show_discipline_permission'
    ]
