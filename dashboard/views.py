# Django imports
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import (ListView)
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from grades.models import Grade, FinalGrade
from django.db.models import Q

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
    context_object_name = 'dashboard'
    permissions_required = [
        'only_teacher_can_change'
    ]

    def get_discipline(self):
        """
        Get the specific discipline.
        """
        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_session(self):
        """
        Take the session that the group belongs to
        """
        discipline = self.get_discipline()

        session = TBLSession.objects.get(
            Q(discipline=discipline),
            Q(pk=self.kwargs.get('pk', ''))
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline and session into context data.
        """
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['session'] = self.get_session()
        return context

    def get_queryset(self):
        """
        Get the questions queryset from model database.
        """
        session = self.get_session()

        grade = Grade.objects.filter(session=session.id)

        return grade
