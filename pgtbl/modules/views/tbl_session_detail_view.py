from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import DetailView

from core.permissions import PermissionMixin
from disciplines.models import Discipline
from modules.models import TBLSession
from modules.utils import get_datetimes


class TBLSessionDetailView(LoginRequiredMixin,
                           PermissionMixin,
                           DetailView):
    """
    View to show a specific tbl session.
    """

    template_name = 'modules/details.html'
    context_object_name = 'session'
    permissions_required = [
        'show_sessions_permission',
        'show_tbl_session'
    ]

    def get_discipline(self):
        """
        Take the discipline that the session belongs to
        """

        discipline = Discipline.objects.get(
            slug=self.kwargs.get('slug', '')
        )

        return discipline

    def get_object(self):
        """
        Get the session discipline.
        """

        discipline = self.get_discipline()

        session = TBLSession.objects.get(
            Q(discipline=discipline),
            Q(pk=self.kwargs.get('pk', ''))
        )

        return session

    def get_context_data(self, **kwargs):
        """
        Insert discipline into tbl session context.
        """

        session = self.get_object()
        irat_datetime, grat_datetime = get_datetimes(session)

        context = super(TBLSessionDetailView, self).get_context_data(**kwargs)
        context['discipline'] = self.get_discipline()
        context['irat_datetime'] = irat_datetime
        context['grat_datetime'] = grat_datetime

        return context
