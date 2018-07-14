from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from TBLSessions.models import TBLSession
from TBLSessions.forms import TBLSessionForm


class TBLSessionListView(LoginRequiredMixin,
                         PermissionMixin,
                         ListView):
    """
    View to see all discipline tbl sessions.
    """

    template_name = 'TBLSessions/list.html'
    paginate_by = 5
    context_object_name = 'sessions'

    permissions_required = [
        'show_sessions_permission'
    ]

    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_context_data(self, **kwargs):
        """
        Insert discipline and form into session context data.
        """

        context = super(TBLSessionListView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['form'] = TBLSessionForm()

        return context

    def get_queryset(self):
        """
        Get the tbl sessions queryset from model database.
        """

        discipline = self.get_discipline()

        sessions = TBLSession.objects.filter(discipline=discipline)

        return sessions
